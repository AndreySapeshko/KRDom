def find_dangling_endpoints(lines):
    """
    Находим висячие концы: endpoints, которые не соединены с другими.
    tol в метрах.
    """
    endpoints = []

    all_pts = []
    for p1, p2 in lines:
        all_pts.append(p1)
        all_pts.append(p2)

    for pt in all_pts:
        count = 0
        for other in all_pts:
            if abs(pt[0] - other[0]) < 1e-6 and abs(pt[1] - other[1]) < 1e-6:
                count += 1

        # endpoint встречается только один раз → висячий
        if count == 1:
            endpoints.append(pt)

    filtered_endpoints = []

    for pt in endpoints:
        count = 0
        for p1, p2 in lines:
            if p1[0] == p2[0] == pt[0] or p1[1] == p2[1] == pt[1]:
                count += 1
        if count == 1:
            filtered_endpoints.append(pt)

    ep_lines = []
    for point in filtered_endpoints:
        for p1, p2 in lines:
            if point == p1 or point == p2:
                if point != p1:
                    p2 = p1

                ep_lines.append((point, p2))

    return ep_lines


def get_verticals_and_horizontals(lines, tol):
    horizontals = []
    verticals = []

    for p1, p2 in lines:
        if abs(p1[1] - p2[1]) < tol:
            horizontals.append((p1, p2))
        elif abs(p1[0] - p2[0]) < tol:
            verticals.append((p1, p2))

    return horizontals, verticals


def restore_missing_door_posts(lines, max_reach=1.2, door_gap=0.7, tol=0.08):
    """
    Восстанавливаем пропавшие косяки дверей:

    - берём только dangling endpoints
    - ищем перпендикулярную стену впереди
    - достраиваем стену так, чтобы остался проём door_gap
    """

    horizontals, verticals = get_verticals_and_horizontals(lines, tol)

    dangling = find_dangling_endpoints(lines)

    new_lines = lines
    np1 = tuple()
    np2 = tuple()

    for p1, p2 in dangling:
        if p1[0] == p2[0]:
            for h1, h2 in horizontals:
                if (h1[0] < p1[0] < h2[0]) or (h1[0] > p1[0] > h2[0]):
                    if p1[1] > p2[1]:
                        if h1[1] > p1[1] and door_gap + 0.05 < (h1[1] - p1[1]) < max_reach:

                            np1 = (p1[0], h1[1])
                            np2 = (p1[0], p1[1] + door_gap)

                    if p1[1] < p2[1]:
                        if p1[1] > h1[1] and door_gap + 0.05 < (p1[1] - h1[1]) < max_reach:

                            np1 = (p1[0], h1[1])
                            np2 = (p1[0], p1[1] - door_gap)

        if p1[1] == p2[1]:
            for v1, v2 in verticals:
                if (v1[1] < p1[1] < v2[1]) or (v1[1] > p1[1] > v2[1]):
                    if p1[0] > p2[0]:
                        if v1[0] > p1[0] and door_gap + 0.05 < (v1[0] - p1[0]) < max_reach:

                            np1 = (v1[0], p1[1])
                            np2 = (p1[0] + door_gap, p1[1])

                    if p1[0] < p2[0]:
                        if p1[0] > v1[0] and door_gap + 0.05 < (p1[0] - v1[0]) < max_reach:

                            np1 = (v1[0], p1[1])
                            np2 = (p1[0] - door_gap, p1[1])

        if np1 and np2:
            if (np1, np2) not in new_lines and (np2, np1) not in new_lines:
                new_lines.append((np1, np2))

    return new_lines


def prune_dangling_edges(lines, max_reach=1.2, door_gap=0.7, tol=0.08):
    """
    Удаляет висячие участки стен:
    - если конец стены ни куда не стыкуется
    - если расстояние до поперечной стены в сторону висячего
    конца меньше door_gap и больше max_reach
    """

    horizontals, verticals = get_verticals_and_horizontals(lines, tol)

    dangling = find_dangling_endpoints(lines)

    new_lines = list(lines)
    on_delete = []

    for p1, p2 in dangling:
        if p1[0] == p2[0]:
            for h1, h2 in horizontals:
                if (h1[0] <= p1[0] <= h2[0]) or (h1[0] > p1[0] > h2[0]):
                    if p1[1] > p2[1]:
                        if h1[1] > p1[1] and (door_gap + 0.05 > (h1[1] - p1[1]) or (h1[1] - p1[1]) > max_reach):

                            on_delete.append((p1, p2))

                    if p1[1] < p2[1]:
                        if p1[1] > h1[1] and (door_gap + 0.05 > (p1[1] - h1[1]) or (p1[1] - h1[1]) > max_reach):

                            on_delete.append((p1, p2))

        if p1[1] == p2[1]:
            for v1, v2 in verticals:
                if (v1[1] <= p1[1] <= v2[1]) or (v1[1] > p1[1] > v2[1]):
                    if p1[0] > p2[0]:
                        if v1[0] > p1[0] and (door_gap + 0.05 > (v1[0] - p1[0]) or (v1[0] - p1[0]) > max_reach):

                            on_delete.append((p1, p2))

                    if p1[0] < p2[0]:
                        if p1[0] > v1[0] and (door_gap + 0.05 > (p1[0] - v1[0]) or (p1[0] - v1[0]) > max_reach):

                            on_delete.append((p1, p2))

    filtered_lines = []

    for p1, p2 in new_lines:
        count = 0
        for dp1, dp2 in on_delete:
            if (p1 == dp1 and p2 == dp2) or (p1 == dp2 and p2 == dp1):
                count += 1

        if count == 0:
            filtered_lines.append((p1, p2))

    return filtered_lines
