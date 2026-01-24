from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.utils import _calc_internal_opening
from backend.core.models.enums import ElementEnum, GroupEnum, OpeningTypes


def test_calc_internal_opening(context):
    item = _calc_internal_opening(GroupEnum.INTERNAL_WALLS, context)

    assert item.group is GroupEnum.INTERNAL_WALLS
    assert item.element is ElementEnum.OPENING_FRAME
    assert item.section_id == context.wall_section.section_id
    assert round_lm(item.lm) == 10.08
    assert round_lm(item.lm_with_waste) == 11.09
    assert round_volume(item.volume_m3) == 0.076

    internal_walls = [
        {
            "length": 5.7,
            "openings": [
                {
                    "height": 2.2,
                    "width": 2,
                    "type": OpeningTypes.PORTAL,
                    "quantity": 1,
                }
            ],
        }
    ]

    context.internal_walls = internal_walls
    item = _calc_internal_opening(GroupEnum.INTERNAL_WALLS, context)

    assert round_lm(item.lm) == 2.84
    assert round_lm(item.lm_with_waste) == 3.12
    assert round_volume(item.volume_m3) == 0.021
