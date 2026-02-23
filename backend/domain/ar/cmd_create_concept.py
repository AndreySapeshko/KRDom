import json
from pathlib import Path

from backend.domain.ar.concept_builder import build_concept
from backend.domain.ar.render.svg_renderer_v2 import SvgRenderOptions, render_concept_to_svg_v2

CONCEPTS_DIR = Path(__file__).parent.parent.parent / "tests" / "domain" / "concepts" / "concept_test_v2.json"

# 1) Load JSON
with open(CONCEPTS_DIR, "r", encoding="utf-8") as f:
    concept_json = json.load(f)

# 2) Validate
concept = build_concept(concept_json)

# 3) Render SVG
svg = render_concept_to_svg_v2(concept, SvgRenderOptions(scale=70))

# 4) Save
with open("plan.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("SVG generated: plan.svg")
