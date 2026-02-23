def compute_bbox(lines):
    xs = []
    ys = []
    for p1, p2 in lines:
        xs += [p1[0], p2[0]]
        ys += [p1[1], p2[1]]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    return min_x, min_y, max_x, max_y


def normalize_to_house_centerline(lines, target_w=7.7, target_h=9.7):
    """
    Приводим wall graph (px) к метрам так, чтобы он стал ровно target_w × target_h.
    Возвращаем lines_m.
    """

    min_x, min_y, max_x, max_y = compute_bbox(lines)

    width_px = max_x - min_x
    height_px = max_y - min_y

    sx = target_h / width_px
    sy = target_w / height_px

    lines_m = []

    for p1, p2 in lines:
        x1, y1 = p1
        x2, y2 = p2

        # нормализация: min corner → (0,0)
        x1m = (x1 - min_x) * sx
        y1m = (y1 - min_y) * sy

        x2m = (x2 - min_x) * sx
        y2m = (y2 - min_y) * sy

        lines_m.append(((x1m, y1m), (x2m, y2m)))

    return lines_m
