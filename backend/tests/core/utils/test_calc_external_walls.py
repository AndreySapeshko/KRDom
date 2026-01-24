from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.utils import _calc_external_walls
from backend.core.models.enums import ElementEnum, GroupEnum


def test_calc_external_walls(context):
    item = _calc_external_walls(GroupEnum.EXTERNAL_WALLS, context)

    assert item.group is GroupEnum.EXTERNAL_WALLS
    assert item.element is ElementEnum.STUDS
    assert item.section_id == context.wall_section.section_id
    assert round_lm(item.lm) == 140.59
    assert round_lm(item.lm_with_waste) == 154.65
    assert round_volume(item.volume_m3) == 1.054
