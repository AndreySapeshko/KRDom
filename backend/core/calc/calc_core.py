from backend.core.calc.context import CalcContext
from backend.core.calc.lath import calc_lath
from backend.core.calc.overlaps import calc_overlaps
from backend.core.calc.roof import calc_roof
from backend.core.calc.walls import calc_walls
from backend.core.models.calc_item import CalcItem


def calculate_items(ctx: CalcContext) -> list[CalcItem]:
    items: list[CalcItem] = []

    items += calc_walls(ctx)
    items += calc_overlaps(ctx)
    items += calc_roof(ctx)
    items += calc_lath(ctx)

    return items
