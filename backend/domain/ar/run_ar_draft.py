import asyncio

from backend.domain.ar.render.svg_renderer_v2 import render_concept_to_svg_v2
from backend.domain.brief.schemas.main_brief import ProjectBriefV1
from backend.llm.ar_planner import generate_valid_concept


async def main():
    brief = ProjectBriefV1.example()

    concept = await generate_valid_concept(brief)

    print("VALID CONCEPT GENERATED")

    svg = render_concept_to_svg_v2(concept)

    with open("ar_plan.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    print("Saved: ar_plan.svg")


if __name__ == "__main__":
    asyncio.run(main())
