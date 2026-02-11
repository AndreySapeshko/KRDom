from backend.core.calc.walls_area import calc_walls_area


def test_calc_walls_area(context):
    walls_area = calc_walls_area(context)

    assert walls_area.get("total_external_walls_area") == 86.03
    assert walls_area.get("total_internal_walls_area") == 118.51
