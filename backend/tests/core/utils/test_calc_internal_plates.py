from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.utils import _calc_internal_plates
from backend.core.models.enums import ElementEnum, GroupEnum


def test_calc_internal_plates(context):
    item = _calc_internal_plates(GroupEnum.INTERNAL_WALLS, ElementEnum.PLATES_BOTTOM, context)

    assert item.group is GroupEnum.INTERNAL_WALLS
    assert item.element is ElementEnum.PLATES_BOTTOM
    assert item.section_id == context.wall_section.section_id
    assert round_lm(item.lm) == 18.96
    assert round_lm(item.lm_with_waste) == 20.86
    assert round_volume(item.volume_m3) == 0.142

    item = _calc_internal_plates(GroupEnum.INTERNAL_WALLS, ElementEnum.PLATES_TOP, context)

    assert item.element is ElementEnum.PLATES_TOP
