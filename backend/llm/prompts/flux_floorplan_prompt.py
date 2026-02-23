FLUX_FLOORPLAN_PROMPT = """
Draw a strict black-and-white schematic floor plan with only walls and labels.

House size: rectangle {}m x {}m, single-story.

MANDATORY ROOMS (must include ALL, do not omit):
{}

STRICT RULES:
- Every room must be drawn as a separate enclosed space.
- Every room must have a visible label and area (m²).
- No missing rooms, no extra unlabeled spaces.
- Entrance door at the bottom side
- Living room on the left, bedrooms on the right

Drawing style:
- Black-and-white technical floor plan
- Only walls, doors, windows, labels
- No furniture, no shading, no 3D
- No perspective, only top-down

Negative:
no 3D, no isometric, no furniture, no exterior.
"""
