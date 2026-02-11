from backend.core.calc.usable_area_of_boards import calc_usable_area_of_boards


def test_usable_area_of_boards(context, total_by_section):
    usable_area_of_boards = calc_usable_area_of_boards(context, total_by_section)

    assert usable_area_of_boards == 410
