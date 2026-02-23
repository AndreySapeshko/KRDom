from shapely.geometry import LineString


def build_wall_solids(lines_m, outer_thickness=0.30, inner_thickness=0.15, tol=0.01):
    """
    1. Делим стены на наружные / внутренние
    2. Строим solids разной толщины
    3. Возвращаем список solids (без union)
    """

    if not lines_m:
        return []

    # --- 1. Находим границы дома по центрлинии
    xs = []
    ys = []

    for p1, p2 in lines_m:
        xs.extend([p1[0], p2[0]])
        ys.extend([p1[1], p2[1]])

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    solids = []

    for p1, p2 in lines_m:
        if abs(p1[0] - p2[0]) < 1e-6:
            if abs(p1[1] - min_y) < 1e-6 and (abs(p1[0] - min_x) < 1e-6 or abs(p1[0] - max_x) < 1e-6):
                p1 = (p1[0], p1[1] - outer_thickness / 2)
            if abs(p2[1] - max_y) < 1e-6 and (abs(p2[0] - min_x) < 1e-6 or abs(p2[0] - max_x) < 1e-6):
                p2 = (p2[0], p2[1] + outer_thickness / 2)

        x1, y1 = p1
        x2, y2 = p2

        # Определяем тип стены
        is_outer = False

        # вертикаль
        if abs(x1 - x2) < tol:
            if abs(x1 - min_x) < tol or abs(x1 - max_x) < tol:
                is_outer = True

        # горизонталь
        if abs(y1 - y2) < tol:
            if abs(y1 - min_y) < tol or abs(y1 - max_y) < tol:
                is_outer = True

        thickness = outer_thickness if is_outer else inner_thickness

        wall_line = LineString([p1, p2])
        solid = wall_line.buffer(thickness / 2, cap_style=2)

        solids.append(solid)

    return solids
