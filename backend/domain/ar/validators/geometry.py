from __future__ import annotations

from typing import List, Tuple

Point2D = Tuple[float, float]


def distance(a: Point2D, b: Point2D) -> float:
    ax, ay = a
    bx, by = b
    return ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5


def polygon_area(points: List[Point2D]) -> float:
    """
    Signed polygon area (absolute value is real area).
    """
    area = 0.0
    n = len(points)

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area += x1 * y2 - x2 * y1

    return abs(area) / 2.0


def is_point_inside_bbox(p: Point2D, bbox: Tuple[float, float, float, float]) -> bool:
    x, y = p
    minx, miny, maxx, maxy = bbox
    return minx <= x <= maxx and miny <= y <= maxy


def polygon_bbox(points: List[Point2D]) -> Tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)
