from backend.core.calc.floors_ceilings_area import calc_floors_ceilings_area


def test_floors_ceilings_area(context):
    floors_ceilings_area = calc_floors_ceilings_area(context)

    assert floors_ceilings_area.get("total_ceilings_area") == 42.47
    assert floors_ceilings_area.get("total_floors_area") == 42.47
