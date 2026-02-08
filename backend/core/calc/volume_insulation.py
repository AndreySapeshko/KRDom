from math import ceil, cos, floor, radians, tan

from backend.core.aggregators.rounding import round_dm, round_lm
from backend.core.calc.context import CalcContext
from backend.core.calc.walls_area import get_openings_area
from backend.db.models.material import Material


def calc_external_walls_insulation(ctx: CalcContext) -> float:
    length = ctx.length
    width = ctx.width
    height = ctx.wall_height
    spacing = ctx.stud_spacing
    count_spacing = (ceil(length / spacing) + ceil(width / spacing)) * 2
    print(f"ctx.wall_section.width_mm: {ctx.wall_section.width_mm}")
    print(
        f"count_spacing: {count_spacing}, height * ctx.total_floors: {height * ctx.total_floors}, "
        f"round_dm(spacing): {round_dm(spacing)}"
    )
    total_volume_insulation = (
        count_spacing * height * ctx.total_floors * round_dm(spacing) * ctx.wall_section.width_mm / 1000
    )
    # фронтон
    fronton_length = width if ctx.is_fronton_short else length
    count_spacing = floor(fronton_length / spacing)
    print(
        f"count_spacing: {count_spacing}, (fronton_length / 2 * tan(radians(ctx.roof_pitch_deg)) + 0.4)"
        f": {(fronton_length / 2 * tan(radians(ctx.roof_pitch_deg)) + 0.4)}"
    )
    total_volume_insulation += (
        (fronton_length / 2 * tan(radians(ctx.roof_pitch_deg)) + 0.4)
        * count_spacing
        * round_dm(spacing)
        * ctx.wall_section.width_mm
        / 1000
    )
    openings_area = get_openings_area(ctx.external_openings)
    total_volume_insulation -= openings_area * ctx.wall_section.width_mm / 1000
    return round_lm(total_volume_insulation)


def calc_internal_walls_insulation(ctx: CalcContext) -> float:
    internal_walls_insulation = 0
    spacing = round_dm(ctx.stud_spacing)
    for i_wall in ctx.internal_walls:
        count_spacing = floor(i_wall.length / ctx.stud_spacing)
        internal_walls_insulation += count_spacing * spacing * ctx.wall_height * ctx.wall_section.width_mm / 1000
        openings_area = get_openings_area(i_wall.openings)
        internal_walls_insulation -= openings_area * ctx.wall_section.width_mm / 1000

    return round_lm(internal_walls_insulation)


def calc_overlap_insulation(ctx: CalcContext, material: Material) -> float:
    spacing = ctx.joist_spacing
    length = ctx.length
    width = ctx.width

    if length >= width:
        overlap_length = length
        overlap_width = width
    else:
        overlap_length = width
        overlap_width = length
    count_spacing = ceil(overlap_length / spacing)
    print(f"material.width_mm: {material.width_mm}")
    return round_lm(overlap_width * round_dm(spacing) * count_spacing * material.width_mm / 1000)


def calc_roof_insulation(ctx: CalcContext) -> float:
    roof_length = ctx.length if ctx.is_fronton_short else ctx.width
    front_length = ctx.width if ctx.is_fronton_short else ctx.length
    roof_width = (front_length / 2) / cos(radians(ctx.roof_pitch_deg))
    count_spacing = ceil(roof_length / ctx.rafter_spacing)
    print(f"ctx.roof_section.width_mm: {ctx.roof_section.width_mm}")
    roof_insulation = roof_width * round_dm(ctx.rafter_spacing) * count_spacing * 2 * ctx.roof_section.width_mm / 1000

    return round_lm(roof_insulation)


def calc_volume_insulation(ctx: CalcContext) -> float:
    total_volume_insulation = calc_external_walls_insulation(ctx)
    print(f"total_volume_insulation: {total_volume_insulation}")
    total_volume_insulation += calc_internal_walls_insulation(ctx)
    print(f"total_volume_insulation: {total_volume_insulation}")
    total_volume_insulation += calc_overlap_insulation(ctx, ctx.attic_overlap_section)
    print(f"total_volume_insulation: {total_volume_insulation}")
    total_volume_insulation += calc_overlap_insulation(ctx, ctx.ground_overlap_section)
    print(f"total_volume_insulation: {total_volume_insulation}")
    total_volume_insulation += calc_overlap_insulation(ctx, ctx.interfloor_overlap_section) * (ctx.total_floors - 1)
    print(f"total_volume_insulation: {total_volume_insulation}")
    total_volume_insulation += calc_roof_insulation(ctx)
    print(f"total_volume_insulation: {total_volume_insulation}")

    return round_lm(total_volume_insulation)
