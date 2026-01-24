from math import ceil

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
            lm=lm_rafters,
            lm_with_waste=lm_rafters * ctx.waste_factor,
            volume_m3=lm_rafters * ctx.roof_section.width_m * ctx.roof_section.height_m,
        )
    )

    result.append(
        CalcItem(
            group=GroupEnum.ROOF_STRUCT,
            element=ElementEnum.RIDGE,
            section_id=ctx.roof_section.section_id,
            lm=roof_length,
            lm_with_waste=roof_length * ctx.waste_factor,
            volume_m3=roof_length * ctx.roof_section.width_m * ctx.roof_section.height_m,
        )
    )

    return result
