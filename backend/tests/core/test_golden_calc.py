import json
from pathlib import Path

from backend.core.aggregators.builder import build_calc_result
from backend.core.models.calc_item import CalcItem

GOLDEN_DIR = Path(__file__).parent / "golden"


def load_items(name: str):
    with open(GOLDEN_DIR / f"{name}_items.json", encoding="utf-8") as f:
        data = json.load(f)
    return [CalcItem(**item) for item in data]


def load_expected(name: str):
    with open(GOLDEN_DIR / f"{name}_expected.json", encoding="utf-8") as f:
        return json.load(f)


def assert_json_equal(actual: dict, expected: dict):
    assert actual == expected, f"\nACTUAL:\n{actual}\n\nEXPECTED:\n{expected}"


def test_golden(context, input_data):
    items = load_items("golden_2")
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
