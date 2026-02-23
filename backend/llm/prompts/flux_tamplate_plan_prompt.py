FLUX_TAMPLATE_PLAN_PROMPT = """
You are given a house outline template image.

STRICT RULES:
- Do NOT modify the outer thick black walls.
- Draw ALL interior walls ONLY inside the inner white rectangle.
- Use only orthogonal walls (90-degree angles).
- Keep the drawing clean and schematic for computer vision.
- No furniture, no textures, no shading.

House size (for proportions): {w}m x {l}m, single-story.

MANDATORY ROOMS (must include ALL, each enclosed and labeled with area in m²):
{r}

Label every room clearly and include area (m²).
Output: black-and-white blueprint style, clean lines only.
"""
