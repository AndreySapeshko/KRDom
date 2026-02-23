from dataclasses import dataclass
from typing import Dict, List, Tuple

import cv2
import numpy as np

# -----------------------------
# Data structures
# -----------------------------


@dataclass
class ExtractedRoom:
    id: str
    polygon: List[Tuple[float, float]]
    area_m2: float


@dataclass
class RoomLayout:
    width_m: float
    height_m: float
    rooms: List[ExtractedRoom]


# -----------------------------
# Main extraction pipeline
# -----------------------------


def extract_rooms_from_walls_only(
    image_path: str, house_width_m: float, house_height_m: float, debug_out: str = "debug_rooms.png"
) -> RoomLayout:
    """
    Extract room polygons from a cleaned walls-only floorplan image.

    Assumptions:
    - Outer walls are thick black
    - Interior walls are thick black
    - Thin door arcs may still exist (we remove them)
    """

    # --- Step 1: Load grayscale ---
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise RuntimeError(f"Cannot load image: {image_path}")

    h, w = img.shape

    # --- Step 2: Binary threshold (walls = white) ---
    _, bw = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    # --- Step 3: Remove thin artifacts (door arcs) ---
    # Opening removes small/thin strokes
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    bw_clean = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel_open)

    # Closing reconnects wall gaps
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    bw_clean = cv2.morphologyEx(bw_clean, cv2.MORPH_CLOSE, kernel_close)

    # --- Step 4: Find outer contour of the house ---
    contours, _ = cv2.findContours(bw_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise RuntimeError("No contours found")

    outer = max(contours, key=cv2.contourArea)

    x, y, ww, hh = cv2.boundingRect(outer)

    # масштаб пиксели → метры
    scale_x = house_width_m / ww
    scale_y = house_height_m / hh

    # --- Step 5: Mask inside the house boundary ---
    house_mask = np.zeros_like(bw_clean)
    cv2.drawContours(house_mask, [outer], -1, 255, thickness=-1)

    # --- Step 6: Free space = inside house but not walls ---
    free_space = cv2.bitwise_and(cv2.bitwise_not(bw_clean), house_mask)

    # --- Step 7: Connected components = rooms ---
    num_labels, labels = cv2.connectedComponents(free_space)

    rooms: List[ExtractedRoom] = []

    debug_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    room_index = 1

    for label_id in range(1, num_labels):
        mask = (labels == label_id).astype(np.uint8) * 255

        area_px = cv2.countNonZero(mask)

        # фильтр: убираем мусор
        if area_px < 2000:
            continue

        # найти контур комнаты
        rcnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not rcnts:
            continue

        cnt = max(rcnts, key=cv2.contourArea)

        # аппроксимация полигона
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        poly = cv2.approxPolyDP(cnt, epsilon, True)

        polygon_m = []
        for pt in poly:
            px, py = pt[0]

            # переводим в координаты дома (относительно bbox)
            mx = (px - x) * scale_x
            my = (py - y) * scale_y

            polygon_m.append((round(mx, 3), round(my, 3)))

        # площадь в м² (приблизительно)
        area_m2 = area_px * scale_x * scale_y

        rooms.append(ExtractedRoom(id=f"room_{room_index}", polygon=polygon_m, area_m2=round(area_m2, 2)))

        room_index += 1

        # Debug draw contour
        cv2.drawContours(debug_img, [cnt], -1, (0, 0, 255), 2)

    # --- Save debug image ---
    cv2.imwrite(debug_out, debug_img)
    print("Saved debug:", debug_out)

    return RoomLayout(width_m=house_width_m, height_m=house_height_m, rooms=rooms)


# -----------------------------
# JSON export
# -----------------------------


def layout_to_json(layout: RoomLayout) -> Dict:
    return {
        "version": "1.0",
        "house": {"width_m": layout.width_m, "height_m": layout.height_m},
        "rooms": [{"id": r.id, "polygon": r.polygon, "area_m2": r.area_m2} for r in layout.rooms],
    }


# -----------------------------
# Run test
# -----------------------------

if __name__ == "__main__":
    layout = extract_rooms_from_walls_only(
        image_path="plan_raw.png", house_width_m=8, house_height_m=10, debug_out="debug_rooms.png"
    )

    data = layout_to_json(layout)

    import json

    print(json.dumps(data, indent=2, ensure_ascii=False))
