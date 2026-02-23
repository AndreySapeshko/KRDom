import math
from typing import Any, Dict, List, Tuple


def render_wall_graph_to_svg(
    graph: Dict[str, Any], house_w_m: float, house_h_m: float, scale: float = 80.0, padding: int = 30
) -> str:
    """
    graph:
      wall_segments: [{p1_m:[x,y], p2_m:[x,y]}]
      openings: [{center_m:[x,y], width_m:..., type:"door"|"window"}]
    """

    width_px = int(house_w_m * scale + padding * 2)
    height_px = int(house_h_m * scale + padding * 2)

    def to_px(pt_m: List[float]) -> Tuple[float, float]:
        x_m, y_m = pt_m
        x = padding + x_m * scale
        # SVG y вниз, у нас y вверх -> инверсия
        y = height_px - (padding + y_m * scale)
        return x, y

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_px}" height="{height_px}" '
        f'viewBox="0 0 {width_px} {height_px}">',
        "<defs>",
        "<style>",
        ".wall { stroke: #111; stroke-width: 10; stroke-linecap: square; }",
        ".outer { stroke: #000; stroke-width: 6; fill: none; }",
        ".opening { stroke: #d00; stroke-width: 6; stroke-linecap: round; }",
        ".label { font-family: Arial, sans-serif; font-size: 14px; fill: #333; }",
        "</style>",
        "</defs>",
        '<rect width="100%" height="100%" fill="white"/>',
    ]

    # Optional: draw house bounding box for reference
    x0, y0 = to_px([0, 0])
    x1, y1 = to_px([house_w_m, house_h_m])
    rect_x = min(x0, x1)
    rect_y = min(y0, y1)
    rect_w = abs(x1 - x0)
    rect_h = abs(y1 - y0)
    svg.append(f'<rect class="outer" x="{rect_x}" y="{rect_y}" width="{rect_w}" height="{rect_h}"/>')

    # Draw wall segments
    for i, seg in enumerate(graph.get("wall_segments", []), start=1):
        p1 = seg["p1_m"]
        p2 = seg["p2_m"]
        x1p, y1p = to_px(p1)
        x2p, y2p = to_px(p2)
        svg.append(f'<line class="wall" x1="{x1p:.1f}" y1="{y1p:.1f}" x2="{x2p:.1f}" y2="{y2p:.1f}"/>')

    # Draw openings as red short line centered at center_m with width_m
    for op in graph.get("openings", []):
        cx, cy = op["center_m"]
        w_m = float(op["width_m"])
        t = op.get("type", "opening")

        # We don't yet know wall orientation; infer by finding nearest wall segment
        # Simple heuristic: nearest segment and choose its orientation
        ori = "h"
        best_d = 1e9
        best_seg = None

        for seg in graph.get("wall_segments", []):
            (x1m, y1m), (x2m, y2m) = seg["p1_m"], seg["p2_m"]
            # distance to segment bbox (fast and good enough for debug)
            dx = 0.0
            dy = 0.0
            if cx < min(x1m, x2m):
                dx = min(x1m, x2m) - cx
            elif cx > max(x1m, x2m):
                dx = cx - max(x1m, x2m)
            if cy < min(y1m, y2m):
                dy = min(y1m, y2m) - cy
            elif cy > max(y1m, y2m):
                dy = cy - max(y1m, y2m)
            d = math.hypot(dx, dy)
            if d < best_d:
                best_d = d
                best_seg = seg

        if best_seg:
            x1m, y1m = best_seg["p1_m"]
            x2m, y2m = best_seg["p2_m"]
            if abs(x2m - x1m) < abs(y2m - y1m):
                ori = "v"
            else:
                ori = "h"

        if ori == "h":
            p1m = [cx - w_m / 2, cy]
            p2m = [cx + w_m / 2, cy]
        else:
            p1m = [cx, cy - w_m / 2]
            p2m = [cx, cy + w_m / 2]

        x1p, y1p = to_px(p1m)
        x2p, y2p = to_px(p2m)
        svg.append(f'<line class="opening" x1="{x1p:.1f}" y1="{y1p:.1f}" x2="{x2p:.1f}" y2="{y2p:.1f}"/>')
        svg.append(f'<text class="label" x="{x1p + 4:.1f}" y="{y1p - 6:.1f}">{t} {w_m:.2f}m</text>')

    svg.append("</svg>")
    return "\n".join(svg)
