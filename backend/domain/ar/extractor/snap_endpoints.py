import numpy as np


def snap_endpoints(lines, snap_tol=10):
    """
    lines: [((x1,y1),(x2,y2))]
    snap_tol: px расстояние, внутри которого точки считаются одной вершиной

    Возвращает новый список lines с привязанными узлами.
    """

    # 1) Собираем все endpoints
    points = []
    for p1, p2 in lines:
        points.append(p1)
        points.append(p2)

    points = np.array(points, dtype=np.float32)

    # 2) Кластеризация простым объединением
    clusters = []
    used = np.zeros(len(points), dtype=bool)

    for i in range(len(points)):
        if used[i]:
            continue

        cluster = [points[i]]
        used[i] = True

        for j in range(i + 1, len(points)):
            if used[j]:
                continue

            if np.linalg.norm(points[i] - points[j]) < snap_tol:
                cluster.append(points[j])
                used[j] = True

        clusters.append(cluster)

    # 3) Центры кластеров
    centers = [np.mean(c, axis=0) for c in clusters]

    # 4) Функция: найти ближайший центр
    def snap_point(pt):
        dists = [np.linalg.norm(pt - c) for c in centers]
        return tuple(centers[int(np.argmin(dists))].astype(int))

    # 5) Применяем snapping ко всем сегментам
    snapped = []
    for p1, p2 in lines:
        sp1 = snap_point(np.array(p1))
        sp2 = snap_point(np.array(p2))
        if sp1 != sp2:
            snapped.append((sp1, sp2))

    return snapped
