# flake8: noqa: F401
import pytest

from backend.api.v1.schemas.calc_input import CalcInputV1, InternalWallIn, OpeningIn
from backend.core.calc.context import CalcContext, InternalWall, Opening
from backend.core.models.enums import OpeningTypes
from backend.core.models.materials import MaterialSection
from backend.core.models.totals import SectionTotal
from backend.db.models.material import Material
from backend.tests.domain.fixtures import (
    brief_with_required_window,
    concept_dict,
    concept_missing_window,
    empty_brief,
    layout_rooms,
    valid_concept,
)


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
        wall_section=Material(
            section_id="BOARD_50x150", width_mm=150, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
        ),
        ground_overlap_section=Material(
            section_id="BOARD_50x200", width_mm=200, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
        ),
        interfloor_overlap_section=Material(
            section_id="BOARD_50x200", width_mm=200, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
        ),
        attic_overlap_section=Material(
            section_id="BOARD_50x150", width_mm=150, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
        ),
        roof_section=Material(
            section_id="BOARD_50x200", width_mm=200, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
        ),
        lath_section=Material(
            section_id="BOARD_25x100", width_mm=100, height_mm=25, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
        ),
        counter_lath_section=Material(
            section_id="BAR_50x50", width_mm=50, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
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
            Opening(type=OpeningTypes.WINDOW, height=1.2, width=1.4, quantity=6),
            Opening(type=OpeningTypes.DOOR, height=2.1, width=0.9, quantity=1),
        ],
        internal_walls=[
            InternalWall(length=5.7, openings=[Opening(type=OpeningTypes.DOOR, height=2.1, width=0.9, quantity=2)]),
            InternalWall(length=3.78, openings=[Opening(type=OpeningTypes.DOOR, height=2.1, width=0.9, quantity=1)]),
        ],
    )


@pytest.fixture
def total_by_section():
    return [
        SectionTotal(section_id="BOARD_25x100", lm=257.6, lm_with_waste=283.36, volume_m3=0.644),
        SectionTotal(section_id="BOARD_50x150", lm=517.41, lm_with_waste=569.16, volume_m3=3.88),
        SectionTotal(section_id="BOARD_50x200", lm=277.28, lm_with_waste=305.01, volume_m3=2.772),
    ]


@pytest.fixture
def material():
    return MaterialSection(section_id="BOARD 50x200x6", width_mm=200, height_mm=50, kind="ГОСТ 8486", length_mm=6000)


@pytest.fixture
def input_data():
    return CalcInputV1(
        length=8,
        width=6,
        wall_height=2.7,
        total_floors=1,
        is_fronton_short=True,
        stud_spacing=0.63,
        joist_spacing=0.63,
        rafter_spacing=0.63,
        wall_section_id="BOARD_50x150x6",
        ground_overlap_section_id="BOARD_50x200x6",
        interfloor_overlap_section_id="BOARD_50x200x6",
        attic_overlap_section_id="BOARD_50x150x6",
        roof_section_id="BOARD_50x200x6",
        lath_section_id="BOARD_25x100x6",
        counter_lath_section_id="BAR_50x50x6",
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
            OpeningIn(type=OpeningTypes.WINDOW, width=1.4, height=1.2, quantity=6),
            OpeningIn(type=OpeningTypes.DOOR, width=0.9, height=2.1, quantity=1),
        ],
        internal_walls=[
            InternalWallIn(
                length=5.7, openings=[OpeningIn(type=OpeningTypes.DOOR, width=0.9, height=2.1, quantity=2)]
            ),
            InternalWallIn(
                length=3.78, openings=[OpeningIn(type=OpeningTypes.DOOR, width=0.9, height=2.1, quantity=1)]
            ),
        ],
    )
