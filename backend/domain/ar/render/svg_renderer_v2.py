from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1
from backend.domain.ar.schemas.walls import Wall

Point = Tuple[float, float]


# ----------------------------
# Small geometry helpers
# ----------------------------


def _distance(a: Point, b: Point) -> float:
    return math.hypot(b[0] - a[0], b[1] - a[1])


def _unit(vx: float, vy: float) -> Tuple[float, float]:
    n = math.hypot(vx, vy)
    if n < 1e-9:
        return (0.0, 0.0)
    return (vx / n, vy / n)


def _lerp(a: Point, b: Point, t: float) -> Point:
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _bbox(points: List[Point]) -> Tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return (min(xs), min(ys), max(xs), max(ys))


def _poly_to_path(points: List[Point]) -> str:
    if not points:
        return ""
    cmds = [f"M {points[0][0]:.3f} {points[0][1]:.3f}"]
    for x, y in points[1:]:
        cmds.append(f"L {x:.3f} {y:.3f}")
    cmds.append("Z")
    return " ".join(cmds)


def _svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def point_in_polygon(point: Point, polygon: List[Point]) -> bool:
    # Ray casting
    x, y = point
    inside = False
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xinters = (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1
            if x < xinters:
                inside = not inside
    return inside


def wall_point_at_offset(w_from: Point, w_to: Point, offset_m: float) -> Point:
    length = _distance(w_from, w_to)
    if length < 1e-9:
        return w_from
    t = max(0.0, min(1.0, offset_m / length))
    return _lerp(w_from, w_to, t)


def draw_dimension(
    svg: List[str],
    p1: Point,
    p2: Point,
    offset_vec: Tuple[float, float],
    label: str,
    minx: float,
    maxy: float,
    opt: SvgRenderOptions,
):
    """
    Рисует размер между p1 и p2 со смещением наружу.
    offset_vec задаёт направление (например вверх).
    """

    ox, oy = offset_vec

    # смещённые точки размерной линии
    q1 = (p1[0] + ox, p1[1] + oy)
    q2 = (p2[0] + ox, p2[1] + oy)

    # SVG coords
    P1 = to_svg_point(p1, minx, maxy, opt)
    P2 = to_svg_point(p2, minx, maxy, opt)
    Q1 = to_svg_point(q1, minx, maxy, opt)
    Q2 = to_svg_point(q2, minx, maxy, opt)

    # выносные линии
    svg.append(
        f'<line x1="{P1[0]:.2f}" y1="{P1[1]:.2f}" '
        f'x2="{Q1[0]:.2f}" y2="{Q1[1]:.2f}" '
        f'stroke="black" stroke-width="1" opacity="0.6"/>'
    )
    svg.append(
        f'<line x1="{P2[0]:.2f}" y1="{P2[1]:.2f}" '
        f'x2="{Q2[0]:.2f}" y2="{Q2[1]:.2f}" '
        f'stroke="black" stroke-width="1" opacity="0.6"/>'
    )

    # основная размерная линия
    svg.append(
        f'<line x1="{Q1[0]:.2f}" y1="{Q1[1]:.2f}" '
        f'x2="{Q2[0]:.2f}" y2="{Q2[1]:.2f}" '
        f'stroke="black" stroke-width="1" opacity="0.8"/>'
    )

    # текст размера по центру
    mid = ((q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2)
    M = to_svg_point(mid, minx, maxy, opt)

    svg.append(
        f'<text x="{M[0]:.2f}" y="{M[1] - 4:.2f}" '
        f'text-anchor="middle" font-family="Arial" '
        f'font-size="{opt.dim_text_font_px}" opacity="0.85">'
        f"{_svg_escape(label)}"
        f"</text>"
    )


def draw_dimension_chain(
    svg: List[str],
    coords: List[float],
    fixed: float,
    direction: str,
    offset: float,
    labels: List[str],
    minx: float,
    maxy: float,
    opt: SvgRenderOptions,
):
    """
    Рисует цепочку размеров между соседними координатами осей.

    coords: список координат осей (например x1,x2,x3)
    fixed: фиксированная координата (y для X-цепочки, x для Y-цепочки)
    direction: "x" или "y"
    offset: смещение наружу
    labels: подписи осей (1,2,3 или A,B,C)
    """

    for i in range(len(coords) - 1):
        c1 = coords[i]
        c2 = coords[i + 1]

        dist_m = abs(c2 - c1)
        dist_mm = dist_m * 1000

        label = f"{dist_mm:.0f}"

        if direction == "x":
            # размеры по X: горизонтальная линия
            p1 = (c1, fixed)
            p2 = (c2, fixed)

            draw_dimension(svg, p1, p2, offset_vec=(0, -offset), label=label, minx=minx, maxy=maxy, opt=opt)

        elif direction == "y":
            # размеры по Y: вертикальная линия
            p1 = (fixed, c1)
            p2 = (fixed, c2)

            draw_dimension(svg, p1, p2, offset_vec=(-offset, 0), label=label, minx=minx, maxy=maxy, opt=opt)


def wall_normal_candidates(w_from: Point, w_to: Point) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    # For vector along wall: (dx, dy)
    dx = w_to[0] - w_from[0]
    dy = w_to[1] - w_from[1]
    ux, uy = _unit(dx, dy)
    # Two normals: left and right (relative to direction)
    n1 = (-uy, ux)
    n2 = (uy, -ux)
    return n1, n2


def wall_to_polygon(w_from: Point, w_to: Point, thickness_m: float) -> List[Point]:
    dx = w_to[0] - w_from[0]
    dy = w_to[1] - w_from[1]
    length = math.hypot(dx, dy)
    if length < 1e-9:
        return []
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux  # left normal
    off = thickness_m / 2.0

    p1 = (w_from[0] + nx * off, w_from[1] + ny * off)
    p2 = (w_to[0] + nx * off, w_to[1] + ny * off)
    p3 = (w_to[0] - nx * off, w_to[1] - ny * off)
    p4 = (w_from[0] - nx * off, w_from[1] - ny * off)
    return [p1, p2, p3, p4]


def wall_to_polygon_external_inward(
    footprint: List[Point],
    w_from: Point,
    w_to: Point,
    thickness_m: float,
) -> List[Point]:
    """
    Наружная стена строится внутрь здания.
    Внешняя грань совпадает с footprint.
    """

    inward, outward = inward_outward_normals_for_external_wall(footprint, w_from, w_to)

    # Внешняя линия = как задано (footprint edge)
    p1 = (w_from[0], w_from[1])
    p2 = (w_to[0], w_to[1])

    # Внутренняя линия = смещение inward на толщину стены
    p3 = (
        w_to[0] + inward[0] * thickness_m,
        w_to[1] + inward[1] * thickness_m,
    )
    p4 = (
        w_from[0] + inward[0] * thickness_m,
        w_from[1] + inward[1] * thickness_m,
    )

    return [p1, p2, p3, p4]


def opening_cut_polygon(
    w_from: Point,
    w_to: Point,
    thickness_m: float,
    offset_m: float,
    width_m: float,
) -> List[Point]:
    # rectangle across wall thickness, along wall direction
    length = _distance(w_from, w_to)
    if length < 1e-9:
        return []
    dx = w_to[0] - w_from[0]
    dy = w_to[1] - w_from[1]
    ux, uy = _unit(dx, dy)
    nx, ny = -uy, ux
    off = thickness_m / 2.0

    s = wall_point_at_offset(w_from, w_to, offset_m)
    e = wall_point_at_offset(w_from, w_to, offset_m + width_m)

    p1 = (s[0] + nx * off, s[1] + ny * off)
    p2 = (e[0] + nx * off, e[1] + ny * off)
    p3 = (e[0] - nx * off, e[1] - ny * off)
    p4 = (s[0] - nx * off, s[1] - ny * off)
    return [p1, p2, p3, p4]


def opening_cut_polygon_external_inward(
    footprint: List[Point],
    w_from: Point,
    w_to: Point,
    thickness_m: float,
    offset_m: float,
    width_m: float,
) -> List[Point]:
    """
    Вырез для наружной стены: внешняя грань по линии стены,
    вырез уходит внутрь на thickness_m.
    """
    inward, outward = inward_outward_normals_for_external_wall(footprint, w_from, w_to)

    s = wall_point_at_offset(w_from, w_to, offset_m)
    e = wall_point_at_offset(w_from, w_to, offset_m + width_m)

    p1 = (s[0], s[1])  # внешняя грань
    p2 = (e[0], e[1])
    p3 = (e[0] + inward[0] * thickness_m, e[1] + inward[1] * thickness_m)
    p4 = (s[0] + inward[0] * thickness_m, s[1] + inward[1] * thickness_m)

    return [p1, p2, p3, p4]


# ----------------------------
# SVG transform
# ----------------------------


@dataclass(frozen=True)
class SvgRenderOptions:
    scale: float = 70.0  # px per meter
    padding_px: float = 60.0

    show_room_labels: bool = True
    show_wall_labels: bool = False
    show_axes: bool = True

    # axes style
    axes_dash: str = "6,6"
    axes_label_font_px: int = 12
    axes_offset_px: float = 18.0
    axes_extension_m: float = 1.0

    # styles
    room_fill_opacity: float = 0.10
    wall_fill_opacity: float = 0.90
    cutout_fill: str = "white"
    show_dimensions: bool = True

    dim_offset_m: float = 0.7  # отступ от дома
    dim_text_font_px: int = 12


def _transform_params(all_points: List[Point], opt: SvgRenderOptions):
    minx, miny, maxx, maxy = _bbox(all_points)
    width_px = (maxx - minx) * opt.scale + 2 * opt.padding_px
    height_px = (maxy - miny) * opt.scale + 2 * opt.padding_px
    return minx, miny, maxx, maxy, width_px, height_px


def to_svg_point(p: Point, minx: float, maxy: float, opt: SvgRenderOptions) -> Point:
    # y inverted for SVG
    x_px = (p[0] - minx) * opt.scale + opt.padding_px
    y_px = (maxy - p[1]) * opt.scale + opt.padding_px
    return (x_px, y_px)


def to_svg_points(points: List[Point], minx: float, maxy: float, opt: SvgRenderOptions) -> List[Point]:
    return [to_svg_point(p, minx, maxy, opt) for p in points]


def centroid(points: List[Point]) -> Point:
    sx = sum(p[0] for p in points)
    sy = sum(p[1] for p in points)
    n = max(1, len(points))
    return (sx / n, sy / n)


# ----------------------------
# Axes (auto-generation)
# ----------------------------


def _unique_sorted(values: List[float], tol: float = 1e-6) -> List[float]:
    vals = sorted(values)
    out: List[float] = []
    for v in vals:
        if not out or abs(v - out[-1]) > tol:
            out.append(v)
    return out


def _y_id(i: int) -> str:
    # A, B, C... (latin)
    return chr(ord("A") + i)


def compute_auto_axes(
    concept: ArchitectureConceptV1, footprint: List[Point]
) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    """
    Автоматически строим оси:
    - X: 1..n по уникальным x из footprint + wall endpoints
    - Y: A.. по уникальным y
    """
    xs: List[float] = [p[0] for p in footprint]
    ys: List[float] = [p[1] for p in footprint]

    for w in concept.walls:
        xs += [w.from_point[0], w.to_point[0]]
        ys += [w.from_point[1], w.to_point[1]]

    ux = _unique_sorted(xs)
    uy = _unique_sorted(ys)

    x_axes = [(str(i + 1), x) for i, x in enumerate(ux)]
    y_axes = [(_y_id(i), y) for i, y in enumerate(uy)]
    return x_axes, y_axes


# ----------------------------
# Door symbol
# ----------------------------


def inward_outward_normals_for_external_wall(
    footprint: List[Point], w_from: Point, w_to: Point
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Для внешней стены пытаемся определить нормаль "внутрь" footprint:
    - берём две нормали n1/n2
    - тестируем точку от середины стены чуть смещённую по нормали
    """
    n1, n2 = wall_normal_candidates(w_from, w_to)
    mid = ((w_from[0] + w_to[0]) / 2.0, (w_from[1] + w_to[1]) / 2.0)
    eps = 0.15  # 15 см

    p1 = (mid[0] + n1[0] * eps, mid[1] + n1[1] * eps)
    p2 = (mid[0] + n2[0] * eps, mid[1] + n2[1] * eps)

    inside1 = point_in_polygon(p1, footprint)
    inside2 = point_in_polygon(p2, footprint)

    if inside1 and not inside2:
        inward = n1
        outward = n2
    elif inside2 and not inside1:
        inward = n2
        outward = n1
    else:
        # fallback: считаем n1 "внутрь"
        inward = n1
        outward = n2

    return inward, outward


def render_concept_to_svg_v2(concept: ArchitectureConceptV1, opt: SvgRenderOptions = SvgRenderOptions()) -> str:
    footprint = concept.building_geometry.footprint.points

    # Collect points for bbox
    all_pts: List[Point] = []
    all_pts += footprint
    for w in concept.walls:
        all_pts += [w.from_point, w.to_point]
    for r in concept.detected_rooms:
        all_pts += r.polygon
    for op in concept.openings:
        # no points; openings are derived
        pass

    minx, miny, maxx, maxy, width_px, height_px = _transform_params(all_pts, opt)

    # wall map
    wall_map: Dict[str, Wall] = {w.id: w for w in concept.walls}

    svg: List[str] = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width_px:.0f}" height="{height_px:.0f}" '
        f'viewBox="0 0 {width_px:.0f} {height_px:.0f}">'
    )

    # background
    svg.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')

    # --- Axes ---
    if opt.show_axes:
        x_axes, y_axes = compute_auto_axes(concept, footprint)

        # --- Axis dimensions X (1-2-3...) ---
        if opt.show_dimensions:
            x_coords = [x for _, x in x_axes]

            # базовая линия под домом
            min_fx, min_fy, max_fx, max_fy = _bbox(footprint)

            chain_offset = opt.dim_offset_m - 0.2

            draw_dimension_chain(
                svg,
                coords=x_coords,
                fixed=min_fy,
                direction="x",
                offset=chain_offset,
                labels=[lab for lab, _ in x_axes],
                minx=minx,
                maxy=maxy,
                opt=opt,
            )
            # --- Axis dimensions Y (A-B-C...) ---
            y_coords = [y for _, y in y_axes]

            draw_dimension_chain(
                svg,
                coords=y_coords,
                fixed=min_fx,
                direction="y",
                offset=chain_offset,
                labels=[lab for lab, _ in y_axes],
                minx=minx,
                maxy=maxy,
                opt=opt,
            )

        # axis extents
        # оси должны выходить за footprint
        ext_px = opt.axes_extension_m * opt.scale

        bx0 = opt.padding_px - ext_px
        by0 = opt.padding_px - ext_px
        bx1 = width_px - opt.padding_px + ext_px
        by1 = height_px - opt.padding_px + ext_px

        label_top_y = opt.padding_px * 0.55
        label_bottom_y = height_px - opt.padding_px * 0.15
        label_left_x = opt.padding_px * 0.45
        label_right_x = width_px - opt.padding_px * 0.15

        # X axes lines (vertical)
        for axis_id, x in x_axes:
            p0 = to_svg_point((x, miny), minx, maxy, opt)
            p1 = to_svg_point((x, maxy), minx, maxy, opt)

            svg.append(
                f'<line x1="{p0[0]:.2f}" y1="{by0:.2f}" '
                f'x2="{p1[0]:.2f}" y2="{by1:.2f}" '
                f'stroke="black" stroke-width="1" opacity="0.25" stroke-dasharray="{opt.axes_dash}"/>'
            )
            # label top/bottom
            svg.append(
                f'<text x="{p0[0]:.2f}" y="{label_top_y:.2f}" text-anchor="middle" '
                f'font-family="Arial" font-size="{opt.axes_label_font_px}" '
                f'opacity="0.75">{_svg_escape(axis_id)}</text>'
            )
            svg.append(
                f'<text x="{p0[0]:.2f}" y="{label_bottom_y:.2f}" text-anchor="middle" '
                f'font-family="Arial" font-size="{opt.axes_label_font_px}" '
                f'opacity="0.75">{_svg_escape(axis_id)}</text>'
            )

        # Y axes lines (horizontal)
        for axis_id, y in y_axes:
            p0 = to_svg_point((minx, y), minx, maxy, opt)
            p1 = to_svg_point((maxx, y), minx, maxy, opt)

            svg.append(
                f'<line x1="{bx0:.2f}" y1="{p0[1]:.2f}" '
                f'x2="{bx1:.2f}" y2="{p1[1]:.2f}" '
                f'stroke="black" stroke-width="1" opacity="0.25" stroke-dasharray="{opt.axes_dash}"/>'
            )
            # label left/right
            svg.append(
                f'<text x="{label_left_x:.2f}" y="{p0[1] + 4:.2f}" text-anchor="middle" '
                f'font-family="Arial" font-size="{opt.axes_label_font_px}" '
                f'opacity="0.75">{_svg_escape(axis_id)}</text>'
            )
            svg.append(
                f'<text x="{label_right_x:.2f}" y="{p0[1] + 4:.2f}" text-anchor="middle" '
                f'font-family="Arial" font-size="{opt.axes_label_font_px}" '
                f'opacity="0.75">{_svg_escape(axis_id)}</text>'
            )

        # --- Dimensions (overall) ---
        if opt.show_dimensions:
            min_fx, min_fy, max_fx, max_fy = _bbox(footprint)

            # offsets наружу
            off = opt.dim_offset_m

            # X dimension (bottom)
            p1 = (min_fx, min_fy)
            p2 = (max_fx, min_fy)

            length_m = max_fx - min_fx
            label_x = f"{length_m * 1000:.0f}"

            draw_dimension(svg, p1, p2, offset_vec=(0, -off), label=label_x, minx=minx, maxy=maxy, opt=opt)

            # Y dimension (left)
            p3 = (min_fx, min_fy)
            p4 = (min_fx, max_fy)

            width_m = max_fy - min_fy
            label_y = f"{width_m * 1000:.0f}"

            draw_dimension(svg, p3, p4, offset_vec=(-off, 0), label=label_y, minx=minx, maxy=maxy, opt=opt)

    # --- Rooms (underlay) ---
    rooms = concept.detected_rooms or []

    for room in rooms:
        cx, cy = room.centroid
        p = to_svg_point((cx, cy), minx, maxy, opt)

        text = room.label or f"{room.net_area_m2:.1f} m²"

        svg.append(
            f'<text x="{p[0]:.2f}" y="{p[1]:.2f}" '
            f'text-anchor="middle" font-family="Arial" '
            f'font-size="14" opacity="0.75">'
            f"{_svg_escape(text)}"
            f"</text>"
        )

    # --- Footprint outline (thin) ---
    fp_svg = to_svg_points(footprint, minx, maxy, opt)
    svg.append(f'<path d="{_poly_to_path(fp_svg)}" fill="none" stroke="black" stroke-width="1.5" opacity="0.6"/>')

    # --- Walls as polygons ---
    for kind in ("external", "internal"):
        for w in concept.walls:
            if w.kind != kind:
                continue

            # наружные стены = extrusion inward-only
            if w.kind == "external":
                poly = wall_to_polygon_external_inward(footprint, w.from_point, w.to_point, w.thickness_m)

            # внутренние стены = centered extrusion
            else:
                poly = wall_to_polygon(w.from_point, w.to_point, w.thickness_m)

            pts_svg = to_svg_points(poly, minx, maxy, opt)
            d = _poly_to_path(pts_svg)

            svg.append(f'<path d="{d}" fill="black" fill-opacity="{opt.wall_fill_opacity:.2f}"/>')

    # --- Openings as cutouts + symbols ---
    for op in concept.openings:
        wall = wall_map.get(op.wall_id)
        if wall is None:
            continue

        # cutout polygon
        if wall.kind == "external":
            cut = opening_cut_polygon_external_inward(
                footprint, wall.from_point, wall.to_point, wall.thickness_m, op.offset_m, op.width_m
            )
        else:
            cut = opening_cut_polygon(wall.from_point, wall.to_point, wall.thickness_m, op.offset_m, op.width_m)
        if not cut:
            continue

        cut_svg = to_svg_points(cut, minx, maxy, opt)
        cut_path = _poly_to_path(cut_svg)

        # 1) cut (white)
        svg.append(f'<path d="{cut_path}" fill="{opt.cutout_fill}"/>')

        # wall direction (unit)
        dx = wall.to_point[0] - wall.from_point[0]
        dy = wall.to_point[1] - wall.from_point[1]
        ux, uy = _unit(dx, dy)

        # normal
        if wall.kind == "external":
            inward, outward = inward_outward_normals_for_external_wall(footprint, wall.from_point, wall.to_point)
        else:
            # internal: pick left as "in", right as "out" (MVP)
            n1, n2 = wall_normal_candidates(wall.from_point, wall.to_point)
            inward, outward = n1, n2

        # start/end points on centerline (world)
        p_start = wall_point_at_offset(wall.from_point, wall.to_point, op.offset_m)
        p_end = wall_point_at_offset(wall.from_point, wall.to_point, op.offset_m + op.width_m)

        # WINDOW: draw thin double-line within opening (rough CAD symbol)
        if op.type == "window":
            sym_off1 = wall.thickness_m * 0.25
            sym_off2 = wall.thickness_m * 0.75

            nx, ny = inward

            a1 = (p_start[0] + nx * sym_off1, p_start[1] + ny * sym_off1)
            b1 = (p_end[0] + nx * sym_off1, p_end[1] + ny * sym_off1)

            a2 = (p_start[0] + nx * sym_off2, p_start[1] + ny * sym_off2)
            b2 = (p_end[0] + nx * sym_off2, p_end[1] + ny * sym_off2)

            A1 = to_svg_point(a1, minx, maxy, opt)
            B1 = to_svg_point(b1, minx, maxy, opt)
            A2 = to_svg_point(a2, minx, maxy, opt)
            B2 = to_svg_point(b2, minx, maxy, opt)

            svg.append(
                f'<line x1="{A1[0]:.2f}" y1="{A1[1]:.2f}" '
                f'x2="{B1[0]:.2f}" y2="{B1[1]:.2f}" '
                f'stroke="black" stroke-width="1.2"/>'
            )

            svg.append(
                f'<line x1="{A2[0]:.2f}" y1="{A2[1]:.2f}" '
                f'x2="{B2[0]:.2f}" y2="{B2[1]:.2f}" '
                f'stroke="black" stroke-width="1.2" opacity="0.7"/>'
            )
        # PORTAL: no symbol, just empty opening (optional thin outline)
        elif op.type == "portal":
            svg.append(f'<path d="{cut_path}" fill="none" stroke="black" stroke-width="1" opacity="0.35"/>')

        # DOOR / INTERIOR_DOOR: leaf + swing arc
        elif op.type in ("door", "interior_door"):
            # hinge point & free point along wall depending on hinge_side
            # hinge at start edge of opening or end edge of opening
            if op.hinge_side == "start":
                hinge = p_start
                free_closed = p_end
            else:
                hinge = p_end
                free_closed = p_start

            # Choose swing vector (in/out)
            swing_vec = inward if op.swing_direction == "in" else outward

            # door leaf in open position: from hinge to hinge + swing_vec * width
            leaf_end_open = (hinge[0] + swing_vec[0] * op.width_m, hinge[1] + swing_vec[1] * op.width_m)

            H = to_svg_point(hinge, minx, maxy, opt)
            FC = to_svg_point(free_closed, minx, maxy, opt)
            FO = to_svg_point(leaf_end_open, minx, maxy, opt)

            # leaf line (hinge -> open end)
            svg.append(
                f'<line x1="{H[0]:.2f}" y1="{H[1]:.2f}" x2="{FO[0]:.2f}" '
                f'y2="{FO[1]:.2f}" stroke="black" stroke-width="2"/>'
            )

            # arc from closed free edge to open leaf edge around hinge
            r = op.width_m * opt.scale
            # Sweep flag depends on direction in SVG coordinate system (Y inverted)
            # We'll derive by cross-product in SVG space:
            v1 = (FC[0] - H[0], FC[1] - H[1])
            v2 = (FO[0] - H[0], FO[1] - H[1])
            cross = v1[0] * v2[1] - v1[1] * v2[0]
            sweep = 1 if cross > 0 else 0

            svg.append(
                f'<path d="M {FC[0]:.2f} {FC[1]:.2f} '
                f'A {r:.2f} {r:.2f} 0 0 {sweep} {FO[0]:.2f} {FO[1]:.2f}" '
                f'fill="none" stroke="black" stroke-width="1" opacity="0.6"/>'
            )

        # label
        mid = ((p_start[0] + p_end[0]) / 2, (p_start[1] + p_end[1]) / 2)
        mid_svg = to_svg_point(mid, minx, maxy, opt)
        svg.append(
            f'<text x="{mid_svg[0]:.2f}" y="{mid_svg[1] - 6:.2f}" text-anchor="middle" '
            f'font-family="Arial" font-size="9" opacity="0.65">{_svg_escape(op.id)}</text>'
        )

    svg.append("</svg>")
    return "\n".join(svg)
