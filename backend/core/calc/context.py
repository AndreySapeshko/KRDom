from dataclasses import dataclass

from backend.core.models.enums import OpeningTypes
from backend.core.models.materials import MaterialSection


@dataclass(frozen=True)
class Opening:
    type: OpeningTypes
    width: float
    height: float
    quantity: int = 1


@dataclass(frozen=True)
class InternalWall:
    length: float
    openings: list[Opening]


@dataclass
class CalcContext:
    length: float
    width: float
    wall_height: float
    total_floors: int
    is_fronton_short: bool

    stud_spacing: float
    joist_spacing: float
    rafter_spacing: float

    wall_section: MaterialSection
    ground_overlap_section: MaterialSection
    interfloor_overlap_section: MaterialSection
    attic_overlap_section: MaterialSection
    roof_section: MaterialSection
    lath_section: MaterialSection

    waste_factor: float

    # roof
    roof_pitch_deg: float
    eave_overhang: float
    gable_overhang: float
    lath_step: float

    # overlaps
    has_ground_overlap: bool
    has_interfloor_overlap: bool
    has_attic_overlap: bool

    ground_blocking_rows: int
    interfloor_blocking_rows: int
    attic_blocking_rows: int

    # openings & walls (как требования)
    external_openings: list[Opening]

    internal_walls: list[InternalWall]
