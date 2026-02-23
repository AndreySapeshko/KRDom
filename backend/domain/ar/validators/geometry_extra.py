from typing import List, Tuple

from backend.domain.ar.validators.geometry import polygon_bbox

Point = Tuple[float, float]


def point_in_polygon(point: Point, polygon: List[Point]) -> bool:
    """
    Ray casting algorithm.
    True если точка внутри polygon.
    """
    x, y = point
    inside = False
    # n = len(polygon)

    min_x, min_y, max_x, max_y = polygon_bbox(polygon)
    if min_x <= x <= max_x and min_y <= y <= max_y:
        inside = True

    # for i in range(n):
    #     x1, y1 = polygon[i]
    #     x2, y2 = polygon[(i + 1) % n]
    #
    #     if ((y1 > y) != (y2 > y)):
    #         xinters = (x2 - x1) * (y - y1) / (y2 - y1 + 1e-9) + x1
    #         if x < xinters:
    #             inside = not inside

    return inside
