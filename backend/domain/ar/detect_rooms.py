from typing import List

from shapely.geometry import Polygon
from shapely.ops import unary_union

from backend.domain.ar.render.svg_renderer import Point, wall_to_polygon
from backend.domain.ar.schemas.rooms import Room
from backend.domain.ar.schemas.walls import Wall


def detect_rooms_from_walls(
    footprint: List[Point],
    walls: List[Wall],
) -> List[Room]:
    """
    Returns detected enclosed spaces (rooms).
    """
    footprint_poly = Polygon(footprint)

    wall_polys = [
        Polygon(wall_to_polygon(w.from_point, w.to_point, w.thickness_m)) for w in walls if w.kind == "internal"
    ]

    barrier = unary_union(wall_polys)

    spaces = footprint_poly.difference(barrier)

    # собираем polygons комнат
    if spaces.geom_type == "Polygon":
        polygons = [spaces]

    elif spaces.geom_type == "MultiPolygon":
        polygons = list(spaces.geoms)

    else:
        polygons = [g for g in spaces.geoms if g.geom_type == "Polygon"]

    rooms: list[Room] = []

    for i, poly in enumerate(polygons):
        coords = [(x, y) for x, y in poly.exterior.coords]

        rooms.append(
            Room(
                id=f"R{i + 1}",
                net_area_m2=float(poly.area),
                centroid=(poly.centroid.x, poly.centroid.y),
                boundary_wall_ids=[],
                polygon=coords,
            )
        )

    return rooms
