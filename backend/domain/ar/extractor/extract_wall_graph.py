import cv2
import numpy as np
from skimage.morphology import skeletonize

from backend.domain.ar.extractor.bridge_collinear_gaps import bridge_collinear_gaps
from backend.domain.ar.extractor.build_wall_solids import build_wall_solids
from backend.domain.ar.extractor.extend_to_t_junction import extend_to_t_junction
from backend.domain.ar.extractor.normalize_to_house_centerline import normalize_to_house_centerline
from backend.domain.ar.extractor.orthogonalize import (
    orthogonalize_lines,
    remove_tiny_segments,
    snap_endpoints_to_intersections,
)
from backend.domain.ar.extractor.remove_small_area import remove_small_closed_components
from backend.domain.ar.extractor.restore_missing_door import prune_dangling_edges, restore_missing_door_posts
from backend.domain.ar.extractor.seal_collinear_gaps import (
    normalize_direction_and_deduplication,
    rounding_axis_coordinates,
    seal_collinear_gaps,
)
from backend.domain.ar.extractor.skeleton_to_hough_lines import (
    export_svg,
    merge_lines,
    skeleton_to_lines,
    snap_orthogonal,
)
from backend.domain.ar.extractor.snap_endpoints_axis import snap_endpoints_axis
from backend.domain.ar.render.export_svg_m import export_svg_m
from backend.domain.ar.render.shapely_to_svg import shapely_to_svg

# ============================================================
# 0) detect_house
# ============================================================


def save(path: str, img: np.ndarray) -> None:
    cv2.imwrite(path, img)


def binarize_dark(gray: np.ndarray) -> np.ndarray:
    # Универсальнее фиксированного порога на разных картинках
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 5)
    return bw


def detect_house_bbox(image_path: str, debug_prefix: str):
    gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise RuntimeError(f"Cannot read {image_path}")

    bw = binarize_dark(gray)  # как было: adaptiveThreshold -> белое=тёмное

    h, w = gray.shape

    # 1) УБИВАЕМ тонкие линии (мебель, сантехника, дуги дверей)
    # kernel подбираем от размера: ~0.8% от меньшей стороны
    k_open = max(7, int(min(h, w) * 0.008))
    if k_open % 2 == 0:
        k_open += 1
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (k_open, k_open))
    thick = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel_open, iterations=1)
    save(f"{debug_prefix}_A00_thick_only.png", thick)

    # 2) Склеиваем разрывы внешней стены от окон/проёмов (но уже на thick-only)
    k_close = max(21, int(min(h, w) * 0.03))  # ~3%
    if k_close % 2 == 0:
        k_close += 1
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (k_close, k_close))
    glued = cv2.morphologyEx(thick, cv2.MORPH_CLOSE, kernel_close, iterations=2)
    save(f"{debug_prefix}_A01_house_glued.png", glued)

    contours, _ = cv2.findContours(glued, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise RuntimeError("House contour not found (thick-only glued has no contours)")

    outer = max(contours, key=cv2.contourArea)
    x, y, ww, hh = cv2.boundingRect(outer)

    # небольшой pad
    pad = int(min(ww, hh) * 0.02)
    x = max(0, x - pad)
    y = max(0, y - pad)
    ww = min(w - x, ww + 2 * pad)
    hh = min(h - y, hh + 2 * pad)

    return {"bbox": (x, y, ww, hh), "glued": glued}


# ============================================================
# 1) Skeletonize walls
# ============================================================


def skeletonize_walls(walls_mask: np.ndarray, debug_prefix="debug"):
    """
    walls_mask: binary (255=wall)
    returns skeleton binary mask (1px lines)
    """
    binary = (walls_mask > 0).astype(np.uint8)

    skel = skeletonize(binary).astype(np.uint8) * 255

    cv2.imwrite(f"{debug_prefix}_S00_skeleton.png", skel)
    return skel


def bridge_skeleton(skel):
    h, w = skel.shape

    k = max(5, int(min(h, w) * 0.01))  # ~1%
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, k))

    # соединяем вертикальные разрывы
    bridged = cv2.morphologyEx(skel, cv2.MORPH_CLOSE, kernel, iterations=1)

    return bridged


# ============================================================
# MAIN PIPELINE
# ============================================================


def extract_wall_graph(image_path: str, house_w_m=8, house_h_m=10, debug_prefix="debug"):
    """
    glued_mask = clean walls from your detect_house_bbox()
    """
    glued_mask = detect_house_bbox(image_path, debug_prefix)["glued"]

    # 1) Skeleton
    skel = skeletonize_walls(glued_mask, debug_prefix)
    skel = bridge_skeleton(skel)

    lines = skeleton_to_lines(skel, house_w_m=8, house_h_m=10)
    export_svg(lines, skel.shape[1], skel.shape[0], filename="after_lines.svg")
    lines = snap_orthogonal(lines)
    export_svg(lines, skel.shape[1], skel.shape[0], filename="after_orthogonal.svg")
    lines = merge_lines(lines)

    lines = bridge_collinear_gaps(lines, gap_tol=50)
    export_svg(lines, skel.shape[1], skel.shape[0], filename="after_bridge.svg")
    lines = snap_endpoints_axis(lines, snap_tol=20)
    export_svg(lines, skel.shape[1], skel.shape[0], filename="after_snap.svg")
    lines = snap_endpoints_axis(lines, snap_tol=20)
    export_svg(lines, skel.shape[1], skel.shape[0], filename="after_snap2.svg")
    lines = extend_to_t_junction(lines, tol=20)
    lines = merge_lines(lines)
    lines, x_axes, y_axes = orthogonalize_lines(lines, snap_tol=8)
    lines = snap_endpoints_to_intersections(lines, x_axes, y_axes, tol=12)
    print(f"BEFORE remove_tiny_segments: {len(lines)}")
    lines = remove_tiny_segments(lines)
    print(f"AFTER remove_tiny_segments: {len(lines)}")

    export_svg(lines, skel.shape[1], skel.shape[0])
    print("Saved wall_graph.svg")

    lines_m = normalize_to_house_centerline(lines, target_w=7.7, target_h=9.7)
    print(f"NORMALIZE_TO_HOUSE_CENTERLINE, len(lines_m): {len(lines_m)}")
    lines_m = rounding_axis_coordinates(lines_m)
    print(f"ROUNDING_AXIS_COORDINATES, len(lines_m): {len(lines_m)}")
    lines_m = normalize_direction_and_deduplication(lines_m)
    print(f"NORMALIZE_DIRECTION_AND_DEDUPLICATION, len(lines_m): {len(lines_m)}")
    lines_m, mask_gaps1 = seal_collinear_gaps(lines_m)
    print(f"SEAL_COLLINEAR_GAPS 1, len(lines_m): {len(lines_m)}")
    for _ in range(3):
        lines_m = restore_missing_door_posts(lines_m)
        lines_m, mask_gaps2 = seal_collinear_gaps(lines_m)
        lines_m = prune_dangling_edges(lines_m)
    print(f"AFTER RESTORE/SEAL/PRUNE, len(lines_m): {len(lines_m)}")
    lines_m = remove_small_closed_components(lines_m)
    export_svg_m(lines_m, "debug5_walls_m.svg")

    walls = build_wall_solids(lines_m)
    shapely_to_svg(walls, "debug6_walls_thick.svg")


if __name__ == "__main__":
    # import json
    extract_wall_graph("plan_raw.png", 8, 10, debug_prefix="debug3")
    # print(json.dumps(data, indent=2, ensure_ascii=False))
    # svg = render_wall_graph_to_svg(data, house_w_m=8, house_h_m=10)
    # with open("wall_graph.svg", "w", encoding="utf-8") as f:
    #     f.write(svg)
