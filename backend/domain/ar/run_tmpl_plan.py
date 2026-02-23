import asyncio
from pathlib import Path

from backend.domain.ar.template_generator import generate_house_template
from backend.llm.openrouter_i2i import OpenRouterImageToImageClient, OpenRouterImageToImageConfig

BASE_DIR = Path(__file__).parent.parent.parent.parent


async def main():
    cfg = OpenRouterImageToImageConfig()
    client = OpenRouterImageToImageClient(cfg)

    templ_filename = "template_plan.png"

    generate_house_template(width_m=8, height_m=10, wall_thickness_m=0.3, filename=templ_filename)

    template_path = BASE_DIR / templ_filename

    await client.fill_template(
        template_png_path=template_path,
        out_png_path="plan_raw.png",
        house_width="8",
        house_length="10",
        notes="Entrance at the bottom side; living room on the left.",
    )

    await client.cleanup_walls_only(noisy_plan_png_path="plan_raw.png", out_png_path="plan_walls_only.png")

    print("VALID IMAGE GENERATED")


if __name__ == "__main__":
    asyncio.run(main())
