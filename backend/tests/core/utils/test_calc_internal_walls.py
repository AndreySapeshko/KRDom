from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.utils import _calc_internal_walls
from backend.core.models.enums import ElementEnum, GroupEnum


def test_calc_internal_walls(context):
    item = _calc_internal_walls(GroupEnum.INTERNAL_WALLS, context)

    assert item.group is GroupEnum.INTERNAL_WALLS
    assert item.element is ElementEnum.STUDS
    assert item.section_id == context.wall_section.section_id
    assert round_lm(item.lm) == 43.2
    assert round_lm(item.lm_with_waste) == 47.52
    assert round_volume(item.volume_m3) == 0.324
