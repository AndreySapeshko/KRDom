from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.utils import _calc_wall_plates
from backend.core.models.enums import ElementEnum, GroupEnum


def test_calc_wall_plates(context):
    item = _calc_wall_plates(GroupEnum.EXTERNAL_WALLS, ElementEnum.PLATES_TOP, context)

    assert item.group is GroupEnum.EXTERNAL_WALLS
    assert item.element is ElementEnum.PLATES_TOP
    assert item.section_id == context.wall_section.section_id
    assert round_lm(item.lm) == 56
    assert round_lm(item.lm_with_waste) == 61.6
    assert round_volume(item.volume_m3) == 0.42

    item = _calc_wall_plates(GroupEnum.EXTERNAL_WALLS, ElementEnum.PLATES_BOTTOM, context)

    assert item.group is GroupEnum.EXTERNAL_WALLS
    assert item.element is ElementEnum.PLATES_BOTTOM
    assert item.section_id == context.wall_section.section_id
    assert round_lm(item.lm) == 56
    assert round_lm(item.lm_with_waste) == 61.6
    assert round_volume(item.volume_m3) == 0.42
