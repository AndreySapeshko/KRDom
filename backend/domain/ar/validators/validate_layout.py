from shapely.geometry import Polygon, box

from backend.domain.ar.schemas.room_layout_v1 import RoomLayoutV1
from backend.domain.ar.schemas.room_layout_v2 import RoomLayoutV2


def validate_layout(layout: RoomLayoutV1, footprint: list[tuple[float, float]]):
    fp_poly = Polygon(footprint)

    issues = []

    for r in layout.rooms:
        x1, y1, x2, y2 = r.rect

        if x2 <= x1 or y2 <= y1:
            issues.append(f"{r.id}: invalid rect coordinates")

        if r.area() <= 1.0:
            issues.append(f"{r.id}: too small area")

        room_poly = box(x1, y1, x2, y2)

        if not fp_poly.contains(room_poly):
            issues.append(f"{r.id}: room is outside footprint")

    return issues


def validate_layout_polygons(layout: RoomLayoutV2, footprint: list[tuple[float, float]]):
    fp_poly = Polygon(footprint)

    issues = []

    for r in layout.rooms:

        if r.area() <= 1.0:
            issues.append(f"{r.id}: too small area")

        poly = Polygon(r.polygon.points)
        if not fp_poly.contains(poly):
            issues.append(f"{r.id}: room is outside footprint")

    return issues
