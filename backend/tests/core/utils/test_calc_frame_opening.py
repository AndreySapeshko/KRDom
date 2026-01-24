from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.context import Opening
from backend.core.calc.utils import _calc_frame_opening
from backend.core.models.enums import ElementEnum, GroupEnum, OpeningTypes


def test_calc_frame_opening(context):
    item = _calc_frame_opening(GroupEnum.EXTERNAL_WALLS, context)

    assert item.group is GroupEnum.EXTERNAL_WALLS
    assert item.element is ElementEnum.OPENING_FRAME
    assert item.section_id == context.wall_section.section_id
    assert round_lm(item.lm) == 37.38
    assert round_lm(item.lm_with_waste) == 41.12
    assert round_volume(item.volume_m3) == 0.28

    external_openings = [
        Opening(type=OpeningTypes.PORTAL, height=2.2, width=2.0, quantity=1),
    ]

    context.external_openings = external_openings
    item = _calc_frame_opening(GroupEnum.EXTERNAL_WALLS, context)

    assert round_lm(item.lm) == 2.84
    assert round_lm(item.lm_with_waste) == 3.12
    assert round_volume(item.volume_m3) == 0.021
