from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.lath import calc_lath
from backend.core.models.enums import ElementEnum, GroupEnum


def test_calc_lath(context):
    item = calc_lath(context)[0]

    assert item.group is GroupEnum.ROOF_LATH
    assert item.element is ElementEnum.LATH
    assert item.section_id == context.lath_section.section_id
    assert round_lm(item.lm) == 257.6
    assert round_lm(item.lm_with_waste) == 283.36
    assert round_volume(item.volume_m3) == 0.644

    context.is_fronton_short = False
    item = calc_lath(context)[0]

    assert round_lm(item.lm) == 259.2
    assert round_lm(item.lm_with_waste) == 285.12
    assert round_volume(item.volume_m3) == 0.648
