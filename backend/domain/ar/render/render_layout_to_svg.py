from backend.domain.ar.schemas.room_layout_v1 import RoomLayoutV1


def render_layout_to_svg(layout: RoomLayoutV1, scale: float = 70) -> str:
    padding = 20

    # find bounds
    max_x = max(r.rect[2] for r in layout.rooms)
    max_y = max(r.rect[3] for r in layout.rooms)

    width = max_x * scale + padding * 2
    height = max_y * scale + padding * 2

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]

    for room in layout.rooms:
        x1, y1, x2, y2 = room.rect

        x = padding + x1 * scale
        y = height - (padding + y2 * scale)

        w = (x2 - x1) * scale
        h = (y2 - y1) * scale

        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" ' f'stroke="black" fill="none" stroke-width="2"/>')

        svg.append(f'<text x="{x + 5}" y="{y + 20}" font-size="14">' f"{room.role}</text>")

    svg.append("</svg>")
    return "\n".join(svg)


def polygon_centroid(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def render_layout_to_svg_polygons(layout: RoomLayoutV1, scale: float = 70) -> str:
    padding = 20

    # --- find global bounds ---
    all_x = []
    all_y = []

    for room in layout.rooms:
        for x, y in room.polygon.points:
            all_x.append(x)
            all_y.append(y)

    max_x = max(all_x)
    max_y = max(all_y)

    width = max_x * scale + padding * 2
    height = max_y * scale + padding * 2

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]

    # --- draw each room polygon ---
    for room in layout.rooms:

        # Convert polygon points to SVG format
        points_svg = []

        for x, y in room.polygon.points:
            sx = padding + x * scale
            sy = height - (padding + y * scale)  # flip Y axis

            points_svg.append(f"{sx},{sy}")

        points_str = " ".join(points_svg)

        # Draw polygon outline
        svg.append(f'<polygon points="{points_str}" ' f'stroke="black" fill="none" stroke-width="2"/>')

        # --- label placement: use first vertex as anchor ---
        cx, cy = polygon_centroid(room.polygon.points)

        label_x = padding + cx * scale
        label_y = height - (padding + cy * scale)

        svg.append(f'<text x="{label_x}" y="{label_y}" font-size="14" text-anchor="middle">' f"{room.role}</text>")

    doors = (layout.doors.external_doors + layout.doors.interior_doors) if layout.doors else []
    for door in doors:
        x, y = door.position
        w = door.width_m

        # door line endpoints
        x1 = padding + (x - w / 2) * scale
        x2 = padding + (x + w / 2) * scale
        y_svg = height - (padding + y * scale)

        svg.append(f'<line x1="{x1}" y1="{y_svg}" ' f'x2="{x2}" y2="{y_svg}" ' f'stroke="red" stroke-width="4"/>')

    svg.append("</svg>")
    return "\n".join(svg)
