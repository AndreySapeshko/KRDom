from backend.core.calc.roof_parameters import calc_roof_parameters


def test_roof_parameters(context):
    roof_parameters = calc_roof_parameters(context)

    assert roof_parameters.get("total_roof_area") == 80.86
    assert roof_parameters.get("total_overhang_area") == 22.27
    assert roof_parameters.get("total_roof_perimeter") == 35.98
    assert roof_parameters.get("total_length_ridge") == 9.2
    assert roof_parameters.get("total_length_gable") == 17.58
    assert roof_parameters.get("total_length_eave") == 18.4
