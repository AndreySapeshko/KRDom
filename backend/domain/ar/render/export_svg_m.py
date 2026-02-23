def export_svg_m(lines_m, filename="walls_m.svg", scale=100):
    """
    Рисуем линии в метрах.
    scale: px per meter
    """

    if not lines_m:
        raise ValueError("lines_m is None")
    xs = [p[0] for seg in lines_m for p in seg]
    ys = [p[1] for seg in lines_m for p in seg]

    w = int(max(xs) * scale + 50)
    h = int(max(ys) * scale + 50)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]

    for p1, p2 in lines_m:
        x1, y1 = p1
        x2, y2 = p2

        svg.append(
            f'<line x1="{x1 * scale}" y1="{y1 * scale}" '
            f'x2="{x2 * scale}" y2="{y2 * scale}" '
            f'stroke="black" stroke-width="2"/>'
        )

    # подпись размеров
    svg.append(f'<text x="10" y="20" font-size="14">' f"Centerline size: {max(xs):.2f}m × {max(ys):.2f}m" f"</text>")

    svg.append("</svg>")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print("Saved:", filename)
