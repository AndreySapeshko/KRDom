from math import ceil

from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.context import CalcContext
from backend.core.calc.utils import _get_length_width_roof
from backend.core.models.calc_item import CalcItem
from backend.core.models.enums import ElementEnum, GroupEnum


def calc_roof(ctx: CalcContext) -> list[CalcItem]:
    roof_length, roof_width = _get_length_width_roof(ctx)
    lm_rafters = ceil(roof_length / ctx.rafter_spacing) * roof_width * 2
    result = []
    result.append(
        CalcItem(
            group=GroupEnum.ROOF_STRUCT,
            element=ElementEnum.RAFTERS,
            section_id=ctx.roof_section.section_id,
            lm=round_lm(lm_rafters),
            lm_with_waste=round_lm(lm_rafters * ctx.waste_factor),
            volume_m3=round_volume(lm_rafters * ctx.roof_section.width_mm * ctx.roof_section.height_mm / 1000000),
        )
    )

    result.append(
        CalcItem(
            group=GroupEnum.ROOF_STRUCT,
            element=ElementEnum.RIDGE,
            section_id=ctx.roof_section.section_id,
            lm=round_lm(roof_length),
            lm_with_waste=round_lm(roof_length * ctx.waste_factor),
            volume_m3=round_volume(roof_length * ctx.roof_section.width_mm * ctx.roof_section.height_mm / 1000000),
        )
    )

    result.append(
        CalcItem(
            group=GroupEnum.ROOF_STRUCT,
            element=ElementEnum.COUNTER_LATH,
            section_id=ctx.counter_lath_section.section_id,
            lm=round_lm(lm_rafters),
            lm_with_waste=round_lm(lm_rafters * ctx.waste_factor),
            volume_m3=round_volume(
                lm_rafters * ctx.counter_lath_section.width_mm * ctx.counter_lath_section.height_mm / 1000000
            ),
        )
    )
    # TODO if ties_enabled добавить в затяжки

    return result
