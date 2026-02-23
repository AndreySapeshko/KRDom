import math

import numpy as np


def dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def angle(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.atan2(dy, dx)


def point_line_distance(pt, a, b):
    pt = np.array(pt)
    a = np.array(a)
    b = np.array(b)

    if np.all(a == b):
        return np.linalg.norm(pt - a)

    return np.abs(np.cross(b - a, a - pt)) / np.linalg.norm(b - a)


def merge_collinear_segments_px(segments, angle_eps_deg=5, snap_eps_px=8, line_eps_px=4):

    merged = []
    used = [False] * len(segments)

    angle_eps = math.radians(angle_eps_deg)

    for i in range(len(segments)):
        if used[i]:
            continue

        p1, p2 = segments[i]

        changed = True
        while changed:
            changed = False

            for j in range(len(segments)):
                if used[j] or j == i:
                    continue

                q1, q2 = segments[j]

                # angle check
                a1 = angle(p1, p2)
                a2 = angle(q1, q2)

                if abs(a1 - a2) > angle_eps and abs(abs(a1 - a2) - math.pi) > angle_eps:
                    continue

                # endpoint proximity
                endpoints = [(p1, q1), (p1, q2), (p2, q1), (p2, q2)]
                close = [(A, B) for A, B in endpoints if dist(A, B) < snap_eps_px]

                if not close:
                    continue

                # collinear check
                if point_line_distance(q1, p1, p2) > line_eps_px:
                    continue
                if point_line_distance(q2, p1, p2) > line_eps_px:
                    continue

                # merge by farthest endpoints
                pts = [p1, p2, q1, q2]

                max_d = 0
                best = (p1, p2)

                for A in pts:
                    for B in pts:
                        d = dist(A, B)
                        if d > max_d:
                            max_d = d
                            best = (A, B)

                p1, p2 = best
                used[j] = True
                changed = True

        used[i] = True
        merged.append((p1, p2))

    return merged
