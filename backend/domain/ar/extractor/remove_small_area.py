from shapely.geometry import LineString
from shapely.ops import polygonize, unary_union


def remove_small_closed_components(lines):

    filtered_lines = []

    shapely_lines = [LineString([p1, p2]) for p1, p2 in lines]

    merged = unary_union(shapely_lines)
    polygons = list(polygonize(merged))

    small_polys = [p for p in polygons if p.area < 1.2]

    for p1, p2 in lines:
        seg = LineString([p1, p2])

        remove = False
        for poly in small_polys:
            if poly.buffer(1e-6).contains(seg):
                remove = True
                break

        if not remove:
            filtered_lines.append((p1, p2))

    return filtered_lines
