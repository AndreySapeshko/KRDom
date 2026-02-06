from math import ceil

from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.context import CalcContext
from backend.core.calc.utils import _get_length_width_roof
from backend.core.models.calc_item import CalcItem
from backend.core.models.enums import ElementEnum, GroupEnum


def calc_lath(ctx: CalcContext) -> list[CalcItem]:
    roof_length, roof_width = _get_length_width_roof(ctx)
    n_rows = ceil(roof_width / ctx.lath_step) + 1
    lm_lath = n_rows * roof_length * 2
    return [
        CalcItem(
            group=GroupEnum.ROOF_STRUCT,
            element=ElementEnum.LATH,
            section_id=ctx.lath_section.section_id,
            lm=round_lm(lm_lath),
            lm_with_waste=round_lm(lm_lath * ctx.waste_factor),
            volume_m3=round_volume(lm_lath * ctx.lath_section.width_mm * ctx.lath_section.height_mm / 1000000),
        )
    ]
