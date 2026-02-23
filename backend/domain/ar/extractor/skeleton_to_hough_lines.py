import cv2
import numpy as np


def skeleton_to_lines(skel: np.ndarray, house_w_m=8, house_h_m=10, max_gap=15):
    """
    Превращаем skeleton (1px линии) в набор векторных сегментов.
    """

    min_len = int(min(house_h_m, house_w_m) * 0.015)
    lines = cv2.HoughLinesP(skel, rho=1, theta=np.pi / 180, threshold=30, minLineLength=min_len, maxLineGap=max_gap)

    if lines is None:
        return []

    result = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        result.append(((x1, y1), (x2, y2)))

    return result


def snap_orthogonal(lines, angle_tol=10):
    """
    Все линии приводим к строго горизонтальным или вертикальным.
    """

    snapped = []

    for (x1, y1), (x2, y2) in lines:
        dx = x2 - x1
        dy = y2 - y1

        angle = np.degrees(np.arctan2(dy, dx))

        # горизонталь
        if abs(angle) < angle_tol or abs(angle) > 180 - angle_tol:
            y = int((y1 + y2) / 2)
            snapped.append(((x1, y), (x2, y)))

        # вертикаль
        elif abs(abs(angle) - 90) < angle_tol:
            x = int((x1 + x2) / 2)
            snapped.append(((x, y1), (x, y2)))

    return snapped


def merge_lines(lines, dist_tol=20):
    """
    Склеиваем сегменты в длинные стены.
    """

    merged = []

    used = [False] * len(lines)

    for i in range(len(lines)):
        if used[i]:
            continue

        (x1, y1), (x2, y2) = lines[i]
        used[i] = True

        # собираем все куски на одной линии
        group = [((x1, y1), (x2, y2))]

        for j in range(i + 1, len(lines)):
            if used[j]:
                continue

            (a1, b1), (a2, b2) = lines[j]

            # горизонтальные
            if abs(y1 - b1) < dist_tol and abs(y2 - b2) < dist_tol:
                if abs(a1 - x2) < dist_tol or abs(a2 - x1) < dist_tol:
                    group.append(((a1, b1), (a2, b2)))
                    used[j] = True

            # вертикальные
            if abs(x1 - a1) < dist_tol and abs(x2 - a2) < dist_tol:
                if abs(b1 - y2) < dist_tol or abs(b2 - y1) < dist_tol:
                    group.append(((a1, b1), (a2, b2)))
                    used[j] = True

        # объединяем группу в один сегмент
        xs = [p[0] for seg in group for p in seg]
        ys = [p[1] for seg in group for p in seg]

        merged.append(((min(xs), min(ys)), (max(xs), max(ys))))

    return merged


def export_svg(lines, w, h, filename="wall_graph.svg"):
    """
    Рисуем сегменты как SVG.
    """

    with open(filename, "w") as f:
        f.write(f'<svg width="{w}" height="{h}" ')
        f.write('xmlns="http://www.w3.org/2000/svg">\n')
        f.write('<rect width="100%" height="100%" fill="black"/>\n')

        for (x1, y1), (x2, y2) in lines:
            f.write(f'<line x1="{x1}" y1="{y1}" ' f'x2="{x2}" y2="{y2}" ' f'stroke="lime" stroke-width="2"/>\n')

        f.write("</svg>")
