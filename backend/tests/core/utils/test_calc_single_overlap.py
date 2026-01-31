from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.utils import _calc_single_overlap
from backend.core.models.enums import ElementEnum, GroupEnum


def test_calc_single_overlap(context):
    items = _calc_single_overlap(
        GroupEnum.GROUND_OVERLAP, context.ground_overlap_section, context.ground_blocking_rows, context
    )

    assert len(items) == 3
    for item in items:
        if item.element is ElementEnum.JOISTS:
            assert item.group is GroupEnum.GROUND_OVERLAP
            assert item.section_id == context.ground_overlap_section.section_id
            assert round_lm(item.lm) == 78
            assert round_lm(item.lm_with_waste) == 85.8
            assert round_volume(item.volume_m3) == 0.78

        if item.element is ElementEnum.RIM:
            assert item.group is GroupEnum.GROUND_OVERLAP
            assert item.section_id == context.ground_overlap_section.section_id
            assert round_lm(item.lm) == 28
            assert round_lm(item.lm_with_waste) == 30.8
            assert round_volume(item.volume_m3) == 0.28

        if item.element is ElementEnum.BLOCKING:
            assert item.group is GroupEnum.GROUND_OVERLAP
            assert item.section_id == context.ground_overlap_section.section_id
            assert round_lm(item.lm) == 30.24
            assert round_lm(item.lm_with_waste) == 33.26
            assert round_volume(item.volume_m3) == 0.302
