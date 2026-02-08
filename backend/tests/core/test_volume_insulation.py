from backend.core.calc.volume_insulation import (
    calc_external_walls_insulation,
    calc_internal_walls_insulation,
    calc_overlap_insulation,
    calc_roof_insulation,
    calc_volume_insulation,
)


def test_calc_external_walls_insulation(context):
    external_walls_insulation = calc_external_walls_insulation(context)

    assert external_walls_insulation == 11.41


def test_calc_internal_walls_insulation(context):
    internal_walls_insulation = calc_internal_walls_insulation(context)

    assert internal_walls_insulation == 2.79


def test_calc_roof_insulation(context):
    roof_insulation = calc_roof_insulation(context)

    assert roof_insulation == 11.43


def test_calc_overlap_insulation(context, material):
    overlap_insulation = calc_overlap_insulation(context, material)

    assert overlap_insulation == 9.36


def test_calc_volume_insulation(context):
    volume_insulation = calc_volume_insulation(context)

    assert volume_insulation == 42.01
