def shapely_to_svg(poly, filename="walls.svg", scale=100):
    if not poly:
        raise ValueError("Poly is None")

    x_mins = []
    x_maxs = []
    y_mins = []
    y_maxs = []
    for p in poly:
        minx, miny, maxx, maxy = p.bounds
        x_mins.append(minx)
        x_maxs.append(maxx)
        y_mins.append(miny)
        y_maxs.append(maxy)

    minx = min(x_mins)
    maxx = max(x_maxs)
    miny = min(y_mins)
    maxy = max(y_maxs)

    width = int((maxx - minx) * scale + 60)
    height = int((maxy - miny) * scale + 60)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]

    def transform(x, y):
        """
        Перевод shapely coords → svg coords
        """
        sx = (x - minx) * scale + 30
        sy = (y - miny) * scale + 30  # отражаем по bbox
        return sx, sy

    for p in poly:
        geoms = [p] if p.geom_type == "Polygon" else p.geoms

        for g in geoms:
            pts = [transform(x, y) for x, y in g.exterior.coords]
            path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

            svg.append(f'<polygon points="{path}" fill="none" stroke="black" stroke-width="2"/>')

    svg.append("</svg>")

    with open(filename, "w") as f:
        f.write("\n".join(svg))

    print("Saved:", filename)
