from pathlib import Path

from backend.core.aggregators.builder import build_calc_result
from backend.core.calc.calc_core import calculate_items
from backend.tests.core.test_golden_calc import load_expected

GOLDEN_DIR = Path(__file__).parent / "golden"


def assert_json_equal(actual: dict, expected: dict):
    assert actual == expected, f"\nACTUAL:\n{actual}\n\nEXPECTED:\n{expected}"


def test_golden(context, input_data):
    items = calculate_items(context)
    expected = load_expected("golden_2")

    result = build_calc_result(items, input_data, ctx=context)

    actual = {
        "totals_by_section": [i.dict() for i in result.totals_by_section],
        "totals_by_group": [
            {
                "group": g.group,
                "totals_by_section": [s.dict() for s in g.totals_by_section],
            }
            for g in result.totals_by_group
        ],
        "summary": result.summary.dict(),
    }

    assert_json_equal(actual, expected)
