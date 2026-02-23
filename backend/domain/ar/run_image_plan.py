import asyncio

from backend.domain.ar.generate_floorplan import generate_floorplan_png
from backend.llm.make_flux_floorplan_prompt import make_flux_floorplan_prompt


async def main():
    width = "8"
    length = "10"
    rooms = [
        "1. Living room 25+ m² with panoramic windows",
        "2. Kitchen 13+ m²",
        "3. Bedroom 1 (12+ m²)",
        "4. Bedroom 2 (12+ m²)",
        "5. Bathroom 1 (4+ m²)",
        "6. Bathroom 2 (4+ m²)",
        "7. Entrance hall (5+ m²)",
    ]
    prompt = make_flux_floorplan_prompt(width, length, rooms)

    await generate_floorplan_png(prompt)

    print("VALID IMAGE GENERATED")


if __name__ == "__main__":
    asyncio.run(main())
