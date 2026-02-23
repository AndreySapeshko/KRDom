FLUX_CLEAN_PLAN_PROMPT = """
Clean this floor plan image for computer vision extraction.

STRICT RULES:
- Remove all furniture, all door arcs, symbols, textures, shadows, decorations.
- Keep ONLY walls / partitions / room boundaries.
- Keep outer walls and inner walls as solid black lines/shapes.
- Keep background pure white.
- Remove dimension lines and any non-wall graphics if present.
- If labels exist, you may remove them (walls-only output).

Output only closed wall polygons on white background.
"""
