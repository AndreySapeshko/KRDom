import asyncio

from backend.domain.ar.generate_room_layout import generate_room_layout
from backend.domain.ar.render.render_layout_to_svg import render_layout_to_svg_polygons
from backend.domain.brief.schemas.main_brief import ProjectBriefV1


async def main():
    brief = ProjectBriefV1.example()

    layout = await generate_room_layout(brief)

    print("VALID CONCEPT GENERATED")

    svg = render_layout_to_svg_polygons(layout)

    with open("layout_plan.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    print("Saved: layout_plan.svg")


if __name__ == "__main__":
    asyncio.run(main())
