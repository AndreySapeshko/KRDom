import cv2
import numpy as np


def lines_to_mask(lines, shape, thickness=6):
    """
    Рендерим wall segments обратно в бинарную маску.
    """
    mask = np.zeros(shape, dtype=np.uint8)

    for p1, p2 in lines:
        cv2.line(mask, p1, p2, 255, thickness)

    return mask


def extract_outer_polygon(lines, shape, debug_prefix="debug"):
    mask = lines_to_mask(lines, shape, thickness=10)

    # закрываем мелкие дырки
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    cv2.imwrite(f"{debug_prefix}_outer_mask.png", mask_closed)

    # flood fill снаружи → получить внутренность дома
    h, w = mask_closed.shape
    flood = mask_closed.copy()

    ffmask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood, ffmask, seedPoint=(0, 0), newVal=128)

    # всё что не залито = дом
    house = np.where(flood == 128, 0, 255).astype(np.uint8)

    cv2.imwrite(f"{debug_prefix}_house_filled.png", house)

    contours, _ = cv2.findContours(house, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise RuntimeError("Outer contour not found")

    outer = max(contours, key=cv2.contourArea)

    eps = 0.01 * cv2.arcLength(outer, True)
    poly = cv2.approxPolyDP(outer, eps, True)

    polygon = [(int(x), int(y)) for [[x, y]] in poly]

    overlay = cv2.cvtColor(house, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(overlay, [poly], -1, (0, 0, 255), 3)

    cv2.imwrite(f"{debug_prefix}_outer_polygon.png", overlay)

    return polygon
