from shapely.geometry import LineString
from shapely.ops import unary_union


def remove_small_islands(walls_union, min_area=1.0):
    if walls_union.geom_type == "Polygon":
        return walls_union

    polys = [p for p in walls_union.geoms if p.area > min_area]
    return unary_union(polys)


def build_wall_solids(lines_m, thickness=0.3):

    solids = []

    x_axes = []
    y_axes = []

    # 1) собираем координаты
    for p1, p2 in lines_m:
        x1, y1 = p1
        x2, y2 = p2

        if abs(x1 - x2) < abs(y1 - y2):  # вертикаль
            x_axes.append(round(x1, 2))
        else:  # горизонталь
            y_axes.append(round(y1, 2))

    def lengthen_on_axis(
        n1,
        n2,
    ):
        s1 = (0, 0)
        s2 = (0, 0)
        if n1[0] == n2[0]:
            if n1[1] > n2[1]:
                y = thickness / 2 if round(n1[1], 2) in y_axes else 0
                s1 = (n1[0], n1[1] + y)
                y = thickness / 2 if round(n2[1], 2) in y_axes else 0
                s2 = (n2[0], n2[1] - y)
            else:
                y = thickness / 2 if round(n2[1], 2) in y_axes else 0
                s2 = (n2[0], n2[1] + y)
                y = thickness / 2 if round(n1[1], 2) in y_axes else 0
                s1 = (n1[0], n1[1] - y)
        if n1[1] == n2[1]:
            if n1[0] > n2[0]:
                x = thickness / 2 if round(n1[0], 2) in x_axes else 0
                s1 = (n1[0] + x, n1[1])
                x = thickness / 2 if round(n2[0], 2) in x_axes else 0
                s2 = (n2[0] - x, n2[1])
            else:
                x = thickness / 2 if round(n2[0], 2) in x_axes else 0
                s2 = (n2[0] + x, n2[1])
                x = thickness / 2 if round(n1[0], 2) in x_axes else 0
                s1 = (n1[0] - x, n1[1])
        return [s1, s2]

    for p1, p2 in lines_m:
        line = lengthen_on_axis(p1, p2)
        wall = LineString(line)
        solid = wall.buffer(thickness / 2, cap_style=2)
        solids.append(solid)

    walls_union = unary_union(solids)

    return walls_union
