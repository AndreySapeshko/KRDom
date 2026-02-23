from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

from backend.domain.ar.schemas.main_concept import ArchitectureConceptV1

Point = Tuple[float, float]


@dataclass(frozen=True)
class SvgRenderOptions:
    # масштаб (px на метр)
    scale: float = 60.0
    padding_px: float = 40.0

    # показывать подписи
    show_room_labels: bool = True
    show_wall_labels: bool = False

    # толщина линий в px (если не хотим “реальную толщину”)
    wall_stroke_px_external: float = 6.0
    wall_stroke_px_internal: float = 3.0

    # стиль заливки комнат
    room_fill_opacity: float = 0.10

    # минимальный зазор по углам для визуализации проемов (в px)
    opening_endcap_px: float = 2.0


def _bbox(points: List[Point]) -> Tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def _centroid(points: List[Point]) -> Point:
    # простой centroid для полигона (для подписи комнаты)
    # Если polygon сложный/самопересекается — может быть неточно, но для MVP ок
    x_sum = 0.0
    y_sum = 0.0
    for x, y in points:
        x_sum += x
        y_sum += y
    n = max(1, len(points))
    return (x_sum / n, y_sum / n)


def _poly_to_path(points: List[Point]) -> str:
    if not points:
        return ""
    cmds = [f"M {points[0][0]:.4f} {points[0][1]:.4f}"]
    for x, y in points[1:]:
        cmds.append(f"L {x:.4f} {y:.4f}")
    cmds.append("Z")
    return " ".join(cmds)


def _distance(a: Point, b: Point) -> float:
    ax, ay = a
    bx, by = b
    return math.hypot(bx - ax, by - ay)


def _lerp(a: Point, b: Point, t: float) -> Point:
    ax, ay = a
    bx, by = b
    return (ax + (bx - ax) * t, ay + (by - ay) * t)


def _wall_point_at_offset(w_from: Point, w_to: Point, offset_m: float) -> Point:
    length = _distance(w_from, w_to)
    if length <= 1e-9:
        return w_from
    t = max(0.0, min(1.0, offset_m / length))
    return _lerp(w_from, w_to, t)


def _project_to_svg_transform(
    all_points: List[Point],
    opt: SvgRenderOptions,
) -> Tuple[float, float, float, float, float]:
    """
    Возвращает параметры трансформации world(m) -> svg(px):
    x_px = (x_m - minx)*scale + padding
    y_px = (maxy - y_m)*scale + padding  (инверсия Y)
    Также возвращаем width_px, height_px, scale.
    """
    minx, miny, maxx, maxy = _bbox(all_points)
    width_px = (maxx - minx) * opt.scale + 2 * opt.padding_px
    height_px = (maxy - miny) * opt.scale + 2 * opt.padding_px
    return minx, miny, maxy, width_px, height_px


def _to_svg_point(
    p: Point,
    minx: float,
    maxy: float,
    opt: SvgRenderOptions,
) -> Point:
    x, y = p
    x_px = (x - minx) * opt.scale + opt.padding_px
    y_px = (maxy - y) * opt.scale + opt.padding_px
    return (x_px, y_px)


def _to_svg_points(
    points: List[Point],
    minx: float,
    maxy: float,
    opt: SvgRenderOptions,
) -> List[Point]:
    return [_to_svg_point(p, minx, maxy, opt) for p in points]


def _svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def wall_to_polygon(
    a: Point,
    b: Point,
    thickness_m: float,
) -> List[Point]:
    """
    Превращает wall centerline в прямоугольный polygon стены.
    """

    ax, ay = a
    bx, by = b

    dx = bx - ax
    dy = by - ay
    length = math.hypot(dx, dy)

    if length < 1e-9:
        return []

    # unit normal vector
    nx = -dy / length
    ny = dx / length

    offset = thickness_m / 2

    p1 = (ax + nx * offset, ay + ny * offset)
    p2 = (bx + nx * offset, by + ny * offset)
    p3 = (bx - nx * offset, by - ny * offset)
    p4 = (ax - nx * offset, ay - ny * offset)

    return [p1, p2, p3, p4]


def render_concept_to_svg(
    concept: ArchitectureConceptV1,
    opt: SvgRenderOptions = SvgRenderOptions(),
) -> str:
    """
    Рендерит SVG план:
    - footprint
    - стены
    - комнаты
    - проёмы (окна/двери) как “разрывы” на стене
    """

    footprint_pts = concept.building_geometry.footprint.points

    # собираем все точки для bbox (footprint + walls + rooms)
    all_pts: List[Point] = []
    all_pts += footprint_pts

    for w in concept.walls:
        all_pts.append(w.from_point)
        all_pts.append(w.to_point)

    for r in concept.rooms:
        all_pts += r.polygon

    # terraces в текущей модели могут быть не в concept_models (если добавишь — добавим сюда)

    minx, miny, maxy, width_px, height_px = _project_to_svg_transform(all_pts, opt)

    # map walls
    wall_map: Dict[str, Tuple[Point, Point, str]] = {}
    for w in concept.walls:
        wall_map[w.id] = (w.from_point, w.to_point, w.kind)

    # --- SVG header ---
    svg_parts: List[str] = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width_px:.0f}" height="{height_px:.0f}" '
        f'viewBox="0 0 {width_px:.0f} {height_px:.0f}">'
    )

    # defs (легкая сетка)
    svg_parts.append("<defs>")
    svg_parts.append(
        '<pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">'
        '<path d="M 50 0 L 0 0 0 50" fill="none" stroke="rgba(0,0,0,0.06)" stroke-width="1"/>'
        "</pattern>"
    )
    svg_parts.append("</defs>")

    # фон + сетка
    svg_parts.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')
    svg_parts.append('<rect x="0" y="0" width="100%" height="100%" fill="url(#grid)"/>')

    # --- Rooms (подложка) ---
    for room in concept.rooms:
        pts_svg = _to_svg_points(room.polygon, minx, maxy, opt)
        d = _poly_to_path(pts_svg)
        svg_parts.append(
            f'<path d="{d}" fill="black" fill-opacity="{opt.room_fill_opacity:.2f}" '
            f'stroke="rgba(0,0,0,0.25)" stroke-width="1"/>'
        )

        if opt.show_room_labels:
            cx, cy = _to_svg_point(_centroid(room.polygon), minx, maxy, opt)
            label = room.type
            if room.area_net_m2 is not None:
                label = f"{room.type} ({room.area_net_m2:.1f} m²)"
            svg_parts.append(
                f'<text x="{cx:.2f}" y="{cy:.2f}" text-anchor="middle" '
                f'font-family="Arial" font-size="12" fill="black" opacity="0.85">'
                f"{_svg_escape(label)}"
                f"</text>"
            )

    # --- Footprint outline (контур) ---
    fp_svg = _to_svg_points(footprint_pts, minx, maxy, opt)
    fp_d = _poly_to_path(fp_svg)
    svg_parts.append(f'<path d="{fp_d}" fill="none" stroke="black" stroke-width="2"/>')

    # --- Walls as polygons ---
    for w in concept.walls:
        poly = wall_to_polygon(w.from_point, w.to_point, w.thickness_m)
        pts_svg = _to_svg_points(poly, minx, maxy, opt)
        d = _poly_to_path(pts_svg)

        svg_parts.append(f'<path d="{d}" fill="black" fill-opacity="0.85"/>')

    # --- Openings (improved symbols) ---
    for op in concept.openings:
        if op.wall_id not in wall_map:
            continue

        w_from, w_to, w_kind = wall_map[op.wall_id]
        wall_len = _distance(w_from, w_to)
        if wall_len <= 1e-9:
            continue

        # Opening segment on wall (world coords)
        p_start = _wall_point_at_offset(w_from, w_to, op.offset_m)
        p_end = _wall_point_at_offset(w_from, w_to, op.offset_m + op.width_m)

        # Convert to SVG
        s = _to_svg_point(p_start, minx, maxy, opt)
        e = _to_svg_point(p_end, minx, maxy, opt)

        # Cut wall (white прорезь)
        # cut_w = wall_stroke(w_kind) + opt.opening_endcap_px
        # svg_parts.append(
        #     f'<line x1="{s[0]:.2f}" y1="{s[1]:.2f}" '
        #     f'x2="{e[0]:.2f}" y2="{e[1]:.2f}" '
        #     f'stroke="white" stroke-width="{cut_w:.2f}" '
        #     f'stroke-linecap="square"/>'
        # )

        # ----------------------------
        # Window symbol
        # ----------------------------
        if op.type == "window":
            # двойная линия окна
            svg_parts.append(
                f'<line x1="{s[0]:.2f}" y1="{s[1]:.2f}" '
                f'x2="{e[0]:.2f}" y2="{e[1]:.2f}" '
                f'stroke="black" stroke-width="1.2"/>'
            )
            svg_parts.append(
                f'<line x1="{s[0]:.2f}" y1="{s[1] - 3:.2f}" '
                f'x2="{e[0]:.2f}" y2="{e[1] - 3:.2f}" '
                f'stroke="black" stroke-width="1.0" opacity="0.6"/>'
            )

        # ----------------------------
        # Door symbol
        # ----------------------------
        elif op.type in ("door", "interior_door"):

            # линия двери
            svg_parts.append(
                f'<line x1="{s[0]:.2f}" y1="{s[1]:.2f}" '
                f'x2="{e[0]:.2f}" y2="{e[1]:.2f}" '
                f'stroke="black" stroke-width="1.5"/>'
            )

            radius = op.width_m * opt.scale

            svg_parts.append(
                f'<path d="M {s[0]:.2f} {s[1]:.2f} '
                f"A {radius:.2f} {radius:.2f} 0 0 1 "
                f'{e[0]:.2f} {e[1]:.2f}" '
                f'fill="none" stroke="black" stroke-width="1" opacity="0.5"/>'
            )

        # Label
        mid_svg = ((s[0] + e[0]) / 2, (s[1] + e[1]) / 2)
        svg_parts.append(
            f'<text x="{mid_svg[0]:.2f}" y="{mid_svg[1] - 6:.2f}" '
            f'text-anchor="middle" font-family="Arial" '
            f'font-size="9" fill="black" opacity="0.7">'
            f"{_svg_escape(op.id)}"
            f"</text>"
        )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)
