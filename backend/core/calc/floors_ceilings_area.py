from backend.core.aggregators.rounding import round_lm
from backend.core.calc.context import CalcContext


def calc_floors_ceilings_area(ctx: CalcContext) -> dict:
    wall_thickness = ctx.wall_section.width_mm / 1000
    internal_length = ctx.length - wall_thickness * 2
    internal_width = ctx.width - wall_thickness * 2

    internal_walls_area_to_floor = 0
    for i_wall in ctx.internal_walls:
        internal_walls_area_to_floor += i_wall.length * wall_thickness

    total_floors_area = round_lm(internal_width * internal_length * ctx.total_floors - internal_walls_area_to_floor)

    return {"total_floors_area": total_floors_area, "total_ceilings_area": total_floors_area}
