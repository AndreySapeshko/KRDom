from PIL import Image, ImageDraw


def generate_house_template(
    width_m: float,
    height_m: float,
    wall_thickness_m: float = 0.3,
    scale: int = 100,
    padding_px: int = 50,
    filename: str = "template.png",
):
    """
    Generates a clean rectangular house outline template:

    - Outer wall: black filled rectangle
    - Inner area: white rectangle (usable space)

    Units:
    - meters → pixels via scale
    """

    # Convert meters → pixels
    outer_w = int(height_m * scale)
    outer_h = int(width_m * scale)

    wall_px = int(wall_thickness_m * scale)

    # Total image size with padding
    img_w = outer_w + padding_px * 2
    img_h = outer_h + padding_px * 2

    # Create white canvas
    img = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(img)

    # Outer rectangle coords
    x1 = padding_px
    y1 = padding_px
    x2 = padding_px + outer_w
    y2 = padding_px + outer_h

    # Draw outer wall (filled black)
    draw.rectangle([x1, y1, x2, y2], fill="black")

    # Inner rectangle coords (subtract wall thickness)
    ix1 = x1 + wall_px
    iy1 = y1 + wall_px
    ix2 = x2 - wall_px
    iy2 = y2 - wall_px

    # Draw inner usable space (white)
    draw.rectangle([ix1, iy1, ix2, iy2], fill="white")

    # Save
    img.save(filename)
    print("Template saved:", filename)


if __name__ == "__main__":
    generate_house_template(width_m=8, height_m=10, wall_thickness_m=0.3, filename="house_template.png")
