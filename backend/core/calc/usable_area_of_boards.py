from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.context import CalcContext
from backend.core.models.totals import SectionTotal


def calc_usable_area_of_boards(ctx: CalcContext, totals_by_section: list[SectionTotal]) -> float:
    materials = [
        ctx.wall_section,
        ctx.lath_section,
        ctx.roof_section,
        ctx.attic_overlap_section,
        ctx.ground_overlap_section,
        ctx.interfloor_overlap_section,
    ]
    total_usable_area_of_board = 0
    for section in totals_by_section:
        for material in materials:
            if section.section_id == material.section_id:
                width_m = round_volume(material.width_mm / 1000)
                height_m = round_volume(material.height_mm / 1000)
                total_usable_area_of_board += (width_m + height_m) * 2 * section.lm
                break
    return round_lm(total_usable_area_of_board)
