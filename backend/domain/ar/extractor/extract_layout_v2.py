from typing import Any, Dict, List

import cv2
import numpy as np


def save(path: str, img: np.ndarray) -> None:
    cv2.imwrite(path, img)


def remove_small_components(binary: np.ndarray, min_area_px: int) -> np.ndarray:
    num, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    out = np.zeros_like(binary)
    for i in range(1, num):
        if stats[i, cv2.CC_STAT_AREA] >= min_area_px:
            out[labels == i] = 255
    return out


def binarize_dark(gray: np.ndarray) -> np.ndarray:
    # Универсальнее фиксированного порога на разных картинках
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 5)
    return bw


def detect_house_bbox(gray: np.ndarray, debug_prefix: str):
    bw = binarize_dark(gray)  # как было: adaptiveThreshold -> белое=тёмное

    h, w = gray.shape

    # 1) УБИВАЕМ тонкие линии (мебель, сантехника, дуги дверей)
    # kernel подбираем от размера: ~0.8% от меньшей стороны
    k_open = max(7, int(min(h, w) * 0.008))
    if k_open % 2 == 0:
        k_open += 1
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (k_open, k_open))
    thick = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel_open, iterations=1)
    save(f"{debug_prefix}_A00_thick_only.png", thick)

    # 2) Склеиваем разрывы внешней стены от окон/проёмов (но уже на thick-only)
    k_close = max(21, int(min(h, w) * 0.03))  # ~3%
    if k_close % 2 == 0:
        k_close += 1
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (k_close, k_close))
    glued = cv2.morphologyEx(thick, cv2.MORPH_CLOSE, kernel_close, iterations=2)
    save(f"{debug_prefix}_A01_house_glued.png", glued)

    contours, _ = cv2.findContours(glued, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise RuntimeError("House contour not found (thick-only glued has no contours)")

    outer = max(contours, key=cv2.contourArea)
    x, y, ww, hh = cv2.boundingRect(outer)

    # небольшой pad
    pad = int(min(ww, hh) * 0.02)
    x = max(0, x - pad)
    y = max(0, y - pad)
    ww = min(w - x, ww + 2 * pad)
    hh = min(h - y, hh + 2 * pad)

    return {"bbox": (x, y, ww, hh), "glued": glued}


def build_house_mask(glued) -> np.ndarray:
    contours, _ = cv2.findContours(glued, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    outer = max(contours, key=cv2.contourArea)

    house_mask = np.zeros_like(glued)
    cv2.drawContours(house_mask, [outer], -1, 255, thickness=-1)
    return house_mask


def wall_mask_inside_house(gray: np.ndarray, house_mask: np.ndarray, debug_prefix: str) -> np.ndarray:
    """
    Стены = тёмные толстые элементы внутри bbox дома.
    Здесь можно удалять мусор, но уже безопасно (внешний bbox фиксирован).
    """
    bw = binarize_dark(gray)
    bw = cv2.bitwise_and(bw, house_mask)

    save(f"{debug_prefix}_B00_bw_in_house.png", bw)

    # Удаляем тонкие линии мебели/дуги:
    # 1) лёгкий opening
    k_open = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, k_open, iterations=1)

    # 2) Подклеиваем стены
    k_close = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, k_close, iterations=2)

    # 3) Убираем совсем мелкий мусор (уже после склейки!)
    bw = remove_small_components(bw, min_area_px=2000)

    save(f"{debug_prefix}_B01_walls0.png", bw)
    return bw


def repair_walls(walls: np.ndarray, debug_prefix: str) -> np.ndarray:
    """
    Важно: тут НЕ выкидывать компоненты агрессивно.
    Наша цель — связность стен.
    """
    # kernel подбираем от размеров изображения: чем больше план, тем больше kernel
    h, w = walls.shape
    k = max(9, int(min(h, w) * 0.015))  # ~1.5% от меньшей стороны
    if k % 2 == 0:
        k += 1
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))

    thick = cv2.dilate(walls, kernel, iterations=1)
    closed = cv2.morphologyEx(thick, cv2.MORPH_CLOSE, kernel, iterations=2)
    fixed = cv2.erode(closed, kernel, iterations=1)

    save(f"{debug_prefix}_B02_walls_repaired.png", fixed)
    return fixed


def seal_exterior_openings_floodfill(walls: np.ndarray, debug_prefix: str) -> np.ndarray:
    """
    Закрывает только наружные проёмы.
    Внутренние двери не трогает.
    """

    h, w = walls.shape

    # 1) Инверсия: стены=0, воздух=255
    air = cv2.bitwise_not(walls)

    # 2) Flood-fill снаружи
    flood = air.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)

    cv2.floodFill(flood, mask, seedPoint=(0, 0), newVal=128)

    save(f"{debug_prefix}_H00_flood_outside.png", flood)

    # 3) Outside region = где flood == 128
    outside = (flood == 128).astype(np.uint8) * 255
    save(f"{debug_prefix}_H01_outside_mask.png", outside)

    # 4) Inside air = воздух, который НЕ снаружи
    inside_air = cv2.bitwise_and(air, cv2.bitwise_not(outside))
    save(f"{debug_prefix}_H02_inside_air.png", inside_air)

    # 5) Дом герметичный = стены + заливка внутри
    sealed_house = cv2.bitwise_or(walls, inside_air)

    save(f"{debug_prefix}_H03_house_sealed.png", sealed_house)

    return sealed_house


def close_openings_for_rooms(walls: np.ndarray, debug_prefix: str) -> np.ndarray:
    """
    Закрываем дверные проёмы, чтобы комнаты стали замкнутыми.
    Используем два направления: горизонталь + вертикаль.
    """

    h, w = walls.shape

    # дверь обычно 70–120 см → ~5–10% ширины стены на плане
    k_long = int(min(h, w) * 0.06)  # ~6%
    k_short = int(min(h, w) * 0.008)  # толщина стены

    if k_long % 2 == 0:
        k_long += 1
    if k_short % 2 == 0:
        k_short += 1

    # горизонтальное закрытие (проёмы в вертикальных стенах)
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (k_long, k_short))

    # вертикальное закрытие (проёмы в горизонтальных стенах)
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (k_short, k_long))

    closed_h = cv2.morphologyEx(walls, cv2.MORPH_CLOSE, kernel_h, iterations=1)
    closed = cv2.morphologyEx(closed_h, cv2.MORPH_CLOSE, kernel_v, iterations=1)

    save(f"{debug_prefix}_C00_walls_closed_for_rooms.png", closed)

    return closed


def directional_close(walls: np.ndarray, k_long: int, k_short: int) -> np.ndarray:
    kh = cv2.getStructuringElement(cv2.MORPH_RECT, (k_long, k_short))
    kv = cv2.getStructuringElement(cv2.MORPH_RECT, (k_short, k_long))
    out = cv2.morphologyEx(walls, cv2.MORPH_CLOSE, kh, iterations=1)
    out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, kv, iterations=1)
    return out


def estimate_wall_thickness_px(walls: np.ndarray) -> int:
    # walls: 0/255, белое = стены
    w01 = (walls > 0).astype(np.uint8)
    # distance внутри белых областей до чёрного
    dt = cv2.distanceTransform(w01, cv2.DIST_L2, 3)
    vals = dt[dt > 0]
    if vals.size == 0:
        return 7
    # median*2 ≈ толщина стены
    th = int(np.median(vals) * 2)
    return max(5, min(th, 35))


def close_openings_for_rooms_auto(
    walls: np.ndarray, house_mask: np.ndarray, debug_prefix: str, target_min_rooms: int = 4, target_max_rooms: int = 20
) -> np.ndarray:
    h, w = walls.shape
    k_short = estimate_wall_thickness_px(walls)
    # чуть усилим
    k_short = max(7, k_short | 1)

    # пробуем несколько k_long (важно: намного больше, чем 0.06*min)
    base = min(h, w)
    candidates = [int(base * p) for p in (0.08, 0.10, 0.12, 0.14, 0.16, 0.18)]
    # сделаем нечетными и с разумными границами
    candidates = [max(61, min(201, (c | 1))) for c in candidates]
    candidates = sorted(set(candidates))

    best = None
    best_score = -10

    for k_long in candidates:
        closed = directional_close(walls, k_long=k_long, k_short=k_short)

        free = cv2.bitwise_and(cv2.bitwise_not(closed), house_mask)
        num, _, stats, _ = cv2.connectedComponentsWithStats(free, connectivity=8)

        # сколько “достаточно больших” областей (кандидатов на комнаты)
        house_area = int(np.count_nonzero(house_mask))
        min_area = int(house_area * 0.003)  # 0.3% — чтобы санузлы не выкидывать
        room_like = sum(1 for i in range(1, num) if stats[i, cv2.CC_STAT_AREA] >= min_area)

        # скоринг: хотим попасть в диапазон
        if target_min_rooms <= room_like <= target_max_rooms:
            score = 100 - abs(room_like - target_min_rooms)  # предпочтём ближе к низу
        else:
            # чем ближе к диапазону — тем лучше
            if room_like < target_min_rooms:
                score = -(target_min_rooms - room_like)
            else:
                score = -(room_like - target_max_rooms)

        if score > best_score:
            best_score = score
            best = (k_long, room_like, closed)

    k_long, room_like, closed = best
    save(f"{debug_prefix}_C00_walls_closed_for_rooms.png", closed)
    print(f"[close_auto] k_short={k_short}, chosen k_long={k_long}, room_like={room_like}, candidates={candidates}")
    return closed


def extract_rooms_from_raw(
    image_path: str, house_w_m: float, house_h_m: float, debug_prefix: str = "debug"
) -> Dict[str, Any]:

    gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise RuntimeError(f"Cannot read {image_path}")

    # A) Находим bbox дома первым делом (иначе outer contour ломается)
    det = detect_house_bbox(gray, debug_prefix)
    glued = det["glued"]
    bbox = det["bbox"]
    house_mask = build_house_mask(glued)

    # B) Стены внутри дома
    walls0 = glued

    # C) Repair walls
    walls1 = repair_walls(walls0, debug_prefix)

    walls_sealed = seal_exterior_openings_floodfill(walls1, debug_prefix)

    # D) Close openings (только для сегментации комнат)
    walls_for_rooms = close_openings_for_rooms(walls_sealed, debug_prefix)

    # E) free space = внутри дома минус стены
    free = cv2.bitwise_and(cv2.bitwise_not(walls_for_rooms), house_mask)
    save(f"{debug_prefix}_C01_free_space.png", free)

    # F) Connected components => комнаты
    num, labels, stats, _ = cv2.connectedComponentsWithStats(free, connectivity=8)

    x, y, ww, hh = bbox
    scale_x = house_w_m / ww
    scale_y = house_h_m / hh

    rooms = []
    house_area_px = ww * hh

    overlay = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    rid = 1
    for i in range(1, num):
        area_px = stats[i, cv2.CC_STAT_AREA]

        # фильтр: например, >= 1% площади дома
        if area_px < int(house_area_px * 0.003):
            continue

        mask = (labels == i).astype(np.uint8) * 255
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts:
            continue

        cnt = max(cnts, key=cv2.contourArea)
        eps = 0.01 * cv2.arcLength(cnt, True)
        poly = cv2.approxPolyDP(cnt, eps, True)

        polygon_m: List[List[float]] = []
        for pt in poly:
            px, py = pt[0]
            mx = (px - x) * scale_x
            my = (py - y) * scale_y
            polygon_m.append([round(float(mx), 3), round(float(my), 3)])

        area_m2 = area_px * scale_x * scale_y

        rooms.append({"id": f"room_{rid}", "polygon": polygon_m, "area_m2": round(float(area_m2), 2)})
        rid += 1

        cv2.drawContours(overlay, [cnt], -1, (0, 0, 255), 2)

    save(f"{debug_prefix}_C02_rooms_overlay.png", overlay)

    return {
        "version": "1.0",
        "house": {"width_m": house_w_m, "height_m": house_h_m},
        "rooms": rooms,
        "debug": {"house_bbox_px": {"x": x, "y": y, "w": ww, "h": hh}},
    }


if __name__ == "__main__":
    import json

    data = extract_rooms_from_raw("plan_raw.png", 8, 10, debug_prefix="debug2")
    print(json.dumps(data, indent=2, ensure_ascii=False))
