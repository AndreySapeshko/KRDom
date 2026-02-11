from math import cos, radians, tan

from backend.core.aggregators.rounding import round_lm
from backend.core.calc.context import CalcContext


def calc_building_dimensions(ctx: CalcContext) -> dict:
    if ctx.length >= ctx.width:
        length = ctx.length
        width = ctx.width
    else:
        length = ctx.width
        width = ctx.length

    fronton_length = ctx.width if ctx.is_fronton_short else ctx.length
    fronton_height = fronton_length / 2 * tan(radians(ctx.roof_pitch_deg))

    height_roof = (
        ctx.roof_section.width_mm / 1000
        + ctx.counter_lath_section.width_mm / 1000
        + ctx.lath_section.width_mm / 1000
        + fronton_height
    )
    height = (
        height_roof / cos(radians(ctx.roof_pitch_deg))
        + ctx.ground_overlap_section.width_mm / 1000
        + ctx.wall_height * ctx.total_floors
        + ctx.interfloor_overlap_section.width_mm * (ctx.total_floors - 1) / 1000
        + ctx.attic_overlap_section.width_mm / 1000
    )

    return {
        "width_building": round_lm(width),
        "length_building": round_lm(length),
        "height_building": round_lm(height),
        "roof_pitch_deg": ctx.roof_pitch_deg,
    }
