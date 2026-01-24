from backend.core.calc.calc_core import calculate_items


def test_calculate_items(context):
    items = calculate_items(context)
    for item in items:
        assert item.group is not None
        assert item.section_id is not None
        assert item.element is not None
        assert item.lm is not None
        assert item.lm_with_waste is not None
        assert item.volume_m3 is not None
        print(f"{item.group} {item.element} {item.section_id} lm: {item.lm}, "
              f"lm_with_waste: {item.lm_with_waste}, volume_m3: {item.volume_m3}\n")
