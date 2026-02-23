def bridge_collinear_gaps(lines, gap_tol=40):
    """
    Соединяет большие разрывы между collinear сегментами.
    Работает после merge_lines.
    """

    new_lines = lines[:]

    for i, (p1, p2) in enumerate(lines):
        for j, (q1, q2) in enumerate(lines):
            if i >= j:
                continue

            # вертикальные стены
            if abs(p1[0] - p2[0]) < 3 and abs(q1[0] - q2[0]) < 3:
                if abs(p1[0] - q1[0]) < 5:
                    # gap между концами
                    ys = sorted([p1[1], p2[1], q1[1], q2[1]])
                    gap = ys[2] - ys[1]
                    if 5 < gap < gap_tol:
                        x = int((p1[0] + q1[0]) / 2)
                        new_lines.append(((x, ys[1]), (x, ys[2])))

            # горизонтальные стены
            if abs(p1[1] - p2[1]) < 3 and abs(q1[1] - q2[1]) < 3:
                if abs(p1[1] - q1[1]) < 5:
                    xs = sorted([p1[0], p2[0], q1[0], q2[0]])
                    gap = xs[2] - xs[1]
                    if 5 < gap < gap_tol:
                        y = int((p1[1] + q1[1]) / 2)
                        new_lines.append(((xs[1], y), (xs[2], y)))

    return new_lines
