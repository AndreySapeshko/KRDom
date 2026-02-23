import numpy as np


def cluster_values(values, tol):
    """
    Группируем координаты в кластеры по допуску tol.
    """
    values = sorted(values)
    clusters = []

    for v in values:
        if not clusters:
            clusters.append([v])
        elif abs(v - clusters[-1][-1]) <= tol:
            clusters[-1].append(v)
        else:
            clusters.append([v])

    # возвращаем центры кластеров
    centers = [sum(c) / len(c) for c in clusters]
    return centers


def snap_value(v, centers):
    """
    Находим ближайший центр кластера.
    """
    return min(centers, key=lambda c: abs(v - c))


def orthogonalize_lines(lines, snap_tol=8):
    """
    Приводим все стены к строгим вертикалям/горизонталям.
    """

    vertical_x = []
    horizontal_y = []

    # 1) собираем координаты
    for p1, p2 in lines:
        x1, y1 = p1
        x2, y2 = p2

        if abs(x1 - x2) < abs(y1 - y2):  # вертикаль
            vertical_x.extend([x1, x2])
        else:  # горизонталь
            horizontal_y.extend([y1, y2])

    # 2) строим оси
    x_axes = cluster_values(vertical_x, tol=snap_tol)
    y_axes = cluster_values(horizontal_y, tol=snap_tol)

    # 3) snap всех сегментов
    ortho = []

    for p1, p2 in lines:
        x1, y1 = p1
        x2, y2 = p2

        if abs(x1 - x2) < abs(y1 - y2):  # вертикаль
            x_new = snap_value((x1 + x2) / 2, x_axes)
            ortho.append(((x_new, y1), (x_new, y2)))

        else:  # горизонталь
            y_new = snap_value((y1 + y2) / 2, y_axes)
            ortho.append(((x1, y_new), (x2, y_new)))

    return ortho, x_axes, y_axes


def snap_endpoints_to_intersections(lines, x_axes, y_axes, tol=10):
    """
    Все концы стен притягиваем к ближайшему пересечению осей.
    """

    def snap_point(px, py):
        # ближайшая вертикальная ось
        x_new = min(x_axes, key=lambda x: abs(px - x))
        # ближайшая горизонтальная ось
        y_new = min(y_axes, key=lambda y: abs(py - y))

        # если достаточно близко → snap
        if abs(px - x_new) <= tol:
            px = x_new
        if abs(py - y_new) <= tol:
            py = y_new

        return (px, py)

    snapped = []

    for p1, p2 in lines:
        x1, y1 = p1
        x2, y2 = p2

        p1s = snap_point(x1, y1)
        p2s = snap_point(x2, y2)

        snapped.append((p1s, p2s))

    return snapped


def remove_tiny_segments(lines, min_len=5):
    clean = []
    for p1, p2 in lines:
        if np.hypot(p1[0] - p2[0], p1[1] - p2[1]) >= min_len:
            clean.append((p1, p2))
    return clean
