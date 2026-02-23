from collections import defaultdict


def rounding_axis_coordinates(lines):
    axis_x = []
    axis_y = []

    for p1, p2 in lines:
        if abs(p1[0] - p2[0]) < 1e-6:
            axis_x.append(p1[0])

        if abs(p1[1] - p2[1]) < 1e-6:
            axis_y.append(p1[1])

    norm_axis_lines = []

    for p1, p2 in lines:
        if abs(p1[0] - p2[0]) < 1e-6:
            if p1[0] in axis_x:
                norm_x = round(p1[0] / 0.05, 0) * 0.05
                p1 = (norm_x, p1[1])
                p2 = (norm_x, p2[1])

        if abs(p1[1] - p2[1]) < 1e-6:
            if p1[1] in axis_y:
                norm_y = round(p1[1] / 0.05, 0) * 0.05
                p1 = (p1[0], norm_y)
                p2 = (p2[0], norm_y)

        # norm_axis_lines.append(((round(p1[0], 2), round(p1[1], 2)), (round(p2[0], 2), round(p2[1], 2))))
        norm_axis_lines.append((p1, p2))

    lines = []

    for p1, p2 in norm_axis_lines:
        if abs(p1[0] - p2[0]) < 1e-6:
            if p1[1] in axis_y:
                norm_y = round(p1[1] / 0.05, 0) * 0.05
                p1 = (p1[0], norm_y)

            if p2[1] in axis_y:
                norm_y = round(p2[1] / 0.05, 0) * 0.05
                p2 = (p2[0], norm_y)

        if abs(p1[1] - p2[1]) < 1e-6:
            if p1[0] in axis_x:
                norm_x = round(p1[0] / 0.05, 0) * 0.05
                p1 = (norm_x, p1[1])

            if p2[0] in axis_x:
                norm_x = round(p2[0] / 0.05, 0) * 0.05
                p2 = (norm_x, p2[1])

        lines.append(((round(p1[0], 2), round(p1[1], 2)), (round(p2[0], 2), round(p2[1], 2))))

    return lines


def normalize_direction_and_deduplication(lines):
    norm_lines = []
    for p1, p2 in lines:
        if abs(p1[0] - p2[0]) < 1e-6:
            if p1[1] > p2[1]:
                buf = p1
                p1 = p2
                p2 = buf

        if abs(p1[1] - p2[1]) < 1e-6:
            if p1[0] > p2[0]:
                buf = p1
                p1 = p2
                p2 = buf

        if (p1, p2) not in norm_lines:
            norm_lines.append((p1, p2))

    return norm_lines


def seal_collinear_gaps(lines, max_gap=7.5):
    """
    Временно соединяем стены, если gap похож на дверь.
    max_gap в метрах.
    """

    axis_x = defaultdict(list)
    axis_y = defaultdict(list)

    for p1, p2 in lines:
        if abs(p1[0] - p2[0]) < 1e-6:
            pm = (p1[1] + p2[1]) / 2
            axis_x[p1[0]].append((pm, (p1, p2)))

        if abs(p1[1] - p2[1]) < 1e-6:
            pm = (p1[0] + p2[0]) / 2
            axis_y[p1[1]].append((pm, (p1, p2)))

    mask_gaps = []

    for ax in axis_x.values():
        ax = sorted(ax, key=lambda x: x[0])
        if len(ax) > 1:
            for i in range(len(ax) - 1):
                segment1_end = ax[i][1][1]
                segment2_start = ax[i + 1][1][0]
                gap = segment2_start[1] - segment1_end[1]
                if 0.7 < gap < max_gap:
                    p1 = (segment1_end[0], segment1_end[1])
                    p2 = (segment1_end[0], segment2_start[1])
                    mask_gaps.append((p1, p2))

    for ay in axis_y.values():
        ay = sorted(ay, key=lambda x: x[0])
        if len(ay) > 1:
            for i in range(len(ay) - 1):
                segment1_end = ay[i][1][1]
                segment2_start = ay[i + 1][1][0]
                gap = segment2_start[0] - segment1_end[0]
                if 0.7 < gap < max_gap:
                    p1 = (segment1_end[0], segment1_end[1])
                    p2 = (segment2_start[0], segment1_end[1])
                    mask_gaps.append((p1, p2))

    return lines + mask_gaps, mask_gaps
