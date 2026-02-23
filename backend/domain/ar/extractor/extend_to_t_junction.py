def extend_to_t_junction(lines, tol=20):
    """
    Удлиняет стены так, чтобы они правильно врезались в другие стены (T-junction).
    Проверяет оба конца (p1 и p2).
    """

    new_lines = []

    for p1, p2 in lines:

        p1 = list(p1)
        p2 = list(p2)

        # определяем ориентацию
        vertical = abs(p1[0] - p2[0]) < abs(p1[1] - p2[1])

        for q1, q2 in lines:
            if (q1, q2) == (tuple(p1), tuple(p2)):
                continue

            # --- если текущая линия вертикальная ---
            if vertical:
                x = p1[0]

                # другая линия должна быть горизонтальной
                if abs(q1[1] - q2[1]) < 3:
                    y = q1[1]

                    # пересечение возможно если x внутри горизонтальной стены
                    if min(q1[0], q2[0]) - tol < x < max(q1[0], q2[0]) + tol:

                        # проверяем p1 конец
                        if abs(p1[1] - y) < tol:
                            p1[1] = y

                        # проверяем p2 конец
                        if abs(p2[1] - y) < tol:
                            p2[1] = y

            # --- если текущая линия горизонтальная ---
            else:
                y = p1[1]

                # другая линия должна быть вертикальной
                if abs(q1[0] - q2[0]) < 3:
                    x = q1[0]

                    if min(q1[1], q2[1]) - tol < y < max(q1[1], q2[1]) + tol:

                        # проверяем p1 конец
                        if abs(p1[0] - x) < tol:
                            p1[0] = x

                        # проверяем p2 конец
                        if abs(p2[0] - x) < tol:
                            p2[0] = x

        # сохраняем обновлённый сегмент
        if p1 != p2:
            new_lines.append((tuple(p1), tuple(p2)))

    return new_lines
