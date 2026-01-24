import pytest

from backend.core.calc.context import CalcContext
from backend.core.models.enums import OpeningTypes
from backend.core.models.materials import MaterialSection


@pytest.fixture
def context():
    return CalcContext(
        length=8.0,
        width=6.0,
        wall_height=2.7,
        total_floors=1,
        is_fronton_short=True,
        stud_spacing=0.63,
        joist_spacing=0.63,
        rafter_spacing=0.63,
        wall_section=MaterialSection(
            section_id="BOARD_50x150", width_m=0.15, height_m=0.05, kind="ГОСТ 8683-83, 1-2 сорт", length=6.0
        ),
        ground_overlap_section=MaterialSection(
            section_id="BOARD_50x200", width_m=0.2, height_m=0.05, kind="ГОСТ 8683-83, 1-2 сорт", length=6.0
        ),
        interfloor_overlap_section=MaterialSection(
            section_id="BOARD_50x200", width_m=0.2, height_m=0.05, kind="ГОСТ 8683-83, 1-2 сорт", length=6.0
        ),
        attic_overlap_section=MaterialSection(
            section_id="BOARD_50x150", width_m=0.15, height_m=0.05, kind="ГОСТ 8683-83, 1-2 сорт", length=6.0
        ),
        roof_section=MaterialSection(
            section_id="BOARD_50x200", width_m=0.2, height_m=0.05, kind="ГОСТ 8683-83, 1-2 сорт", length=6.0
        ),
        lath_section=MaterialSection(
            section_id="BOARD_25x100", width_m=0.1, height_m=0.025, kind="ГОСТ 8683-83, 1-2 сорт", length=6.0
        ),
        waste_factor=1.1,
        roof_pitch_deg=35.0,
        eave_overhang=0.6,
        gable_overhang=0.6,
        lath_step=0.35,
        has_ground_overlap=True,
        has_interfloor_overlap=False,
        has_attic_overlap=True,
        ground_blocking_rows=4,
        interfloor_blocking_rows=4,
        attic_blocking_rows=4,
        external_openings=[
            {
                "height": 1.2,
                "width": 1.4,
                "type": OpeningTypes.WINDOW,
                "quantity": 6,
            },
            {
                "height": 2.1,
                "width": 0.9,
                "type": OpeningTypes.DOOR,
                "quantity": 1,
            },
        ],
        internal_walls=[
            {
                "length": 5.7,
                "openings": [
                    {
                        "height": 2.1,
                        "width": 0.9,
                        "type": OpeningTypes.DOOR,
                        "quantity": 2,
                    }
                ],
            },
            {
                "length": 3.78,
                "openings": [
                    {
                        "height": 2.1,
                        "width": 0.9,
                        "type": OpeningTypes.DOOR,
                        "quantity": 1,
                    }
                ],
            },
        ],
    )
