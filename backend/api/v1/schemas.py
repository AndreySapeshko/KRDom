from enum import Enum

from pydantic import BaseModel


class OpeningTypes(str, Enum):
    DOOR = "DOOR"
    WINDOW = "WINDOW"
    PORTAL = "PORTAL"


class OpeningIn(BaseModel):
    type: OpeningTypes
    width: float
    height: float
    quantity: int = 1


class InternalWallIn(BaseModel):
    length: float
    openings: list[OpeningIn] = []


class CalcInputV1(BaseModel):
    length: float
    width: float
    wall_height: float
    total_floors: int = 1
    is_fronton_short: bool = False

    stud_spacing: float
    joist_spacing: float
    rafter_spacing: float

    wall_section_id: str
    ground_overlap_section_id: str
    interfloor_overlap_section_id: str
    attic_overlap_section_id: str
    roof_section_id: str
    lath_section_id: str

    waste_factor: float = 1.1

    roof_pitch_deg: float
    eave_overhang: float
    gable_overhang: float
    lath_step: float
    ties_enabled: bool

    has_ground_overlap: bool = True
    has_interfloor_overlap: bool = False
    has_attic_overlap: bool = True

    ground_blocking_rows: int = 1
    interfloor_blocking_rows: int = 1
    attic_blocking_rows: int = 1

    external_openings: list[OpeningIn] = []
    internal_walls: list[InternalWallIn] = []
