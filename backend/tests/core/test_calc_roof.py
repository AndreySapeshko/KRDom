from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.roof import calc_roof
from backend.core.models.enums import ElementEnum, GroupEnum


def test_calc_roof(context):
    items = calc_roof(context)
    for item in items:
        if item.element is ElementEnum.RAFTERS:
            assert item.group is GroupEnum.ROOF_STRUCT
            assert item.element is ElementEnum.RAFTERS
            assert item.section_id == context.roof_section.section_id
            assert round_lm(item.lm) == 131.84
            assert round_lm(item.lm_with_waste) == 145.03
            assert round_volume(item.volume_m3) == 1.318

        if item.element is ElementEnum.RIDGE:
            assert item.group is GroupEnum.ROOF_STRUCT
            assert item.element is ElementEnum.RIDGE
            assert item.section_id == context.roof_section.section_id
            assert round_lm(item.lm) == 9.2
            assert round_lm(item.lm_with_waste) == 10.12
            assert round_volume(item.volume_m3) == 0.092

    context.is_fronton_short = False
    items = calc_roof(context)
    for item in items:
        if item.element is ElementEnum.RAFTERS:
            assert round_lm(item.lm) == 134.77
            assert round_lm(item.lm_with_waste) == 148.25
            assert round_volume(item.volume_m3) == 1.348

        if item.element is ElementEnum.RIDGE:
            assert round_lm(item.lm) == 7.2
            assert round_lm(item.lm_with_waste) == 7.92
            assert round_volume(item.volume_m3) == 0.072
