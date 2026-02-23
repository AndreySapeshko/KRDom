import numpy as np


def snap_endpoints_axis(lines, snap_tol=20):
    """
    Snapping, который сохраняет ориентацию стен.
    """

    # Собираем все endpoints
    pts = []
    for p1, p2 in lines:
        pts.append(p1)
        pts.append(p2)

    pts = np.array(pts, dtype=np.float32)

    # Кластеризация точек
    clusters = []
    used = np.zeros(len(pts), dtype=bool)

    for i in range(len(pts)):
        if used[i]:
            continue

        cluster_idx = [i]
        used[i] = True

        for j in range(i + 1, len(pts)):
            if used[j]:
                continue

            if np.linalg.norm(pts[i] - pts[j]) < snap_tol:
                cluster_idx.append(j)
                used[j] = True

        clusters.append(cluster_idx)

    # Центры кластеров
    centers = []
    for idxs in clusters:
        c = np.mean(pts[idxs], axis=0)
        centers.append(c)

    # Snap point → ближайший центр
    def nearest_center(pt):
        dists = [np.linalg.norm(pt - c) for c in centers]
        return centers[int(np.argmin(dists))]

    snapped_lines = []

    for p1, p2 in lines:
        p1 = np.array(p1, dtype=np.float32)
        p2 = np.array(p2, dtype=np.float32)

        # ориентация сегмента
        dx = abs(p2[0] - p1[0])
        dy = abs(p2[1] - p1[1])

        vertical = dx < dy

        c1 = nearest_center(p1)
        c2 = nearest_center(p2)

        if vertical:
            # вертикальная: x одинаковый
            x = int((c1[0] + c2[0]) / 2)
            y1 = int(c1[1])
            y2 = int(c2[1])
            snapped_lines.append(((x, y1), (x, y2)))

        else:
            # горизонтальная: y одинаковый
            y = int((c1[1] + c2[1]) / 2)
            x1 = int(c1[0])
            x2 = int(c2[0])
            snapped_lines.append(((x1, y), (x2, y)))

    return snapped_lines
