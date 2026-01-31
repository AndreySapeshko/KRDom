from backend.core.aggregators.rounding import round_lm
from backend.core.calc.utils import _get_length_width_roof


def test_get_length_width_roof(context):
    roof_length, roof_width = _get_length_width_roof(context)

    assert round_lm(roof_width) == 4.39
    assert roof_length == 9.2

    context.is_fronton_short = False
    roof_length, roof_width = _get_length_width_roof(context)

    assert round_lm(roof_width) == 5.62
    assert roof_length == 7.2
