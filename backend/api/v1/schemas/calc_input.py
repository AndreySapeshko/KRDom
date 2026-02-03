from enum import Enum

from pydantic import BaseModel, Field, model_validator


class OpeningTypes(str, Enum):
    DOOR = "DOOR"
    WINDOW = "WINDOW"
    PORTAL = "PORTAL"


class OpeningIn(BaseModel):
    type: OpeningTypes = "WINDOW"
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    quantity: int = 1


class InternalWallIn(BaseModel):
    length: float = Field(..., gt=0)
    openings: list[OpeningIn] = []


class CalcInputV1(BaseModel):
    length: float = Field(..., gt=0)
    width: float = Field(..., gt=0)
    wall_height: float = Field(..., gt=0)
    total_floors: int = 1
    is_fronton_short: bool = True

    stud_spacing: float = Field(..., gt=0)
    joist_spacing: float = Field(..., gt=0)
    rafter_spacing: float = Field(..., gt=0)

    wall_section_id: str = "BOARD_50x150x6"
    ground_overlap_section_id: str = "BOARD_50x200x6"
    interfloor_overlap_section_id: str = "BOARD_50x200x6"
    attic_overlap_section_id: str = "BOARD_50x150x6"
    roof_section_id: str = "BOARD_50x200x6"
    lath_section_id: str = "BOARD_25x100x6"

    waste_factor: float = 1.1

    roof_pitch_deg: float = Field(..., ge=5, le=60)
    eave_overhang: float = 0.6
    gable_overhang: float = 0.6
    lath_step: float = 0.35
    ties_enabled: bool = False

    has_ground_overlap: bool = True
    has_interfloor_overlap: bool = False
    has_attic_overlap: bool = True

    ground_blocking_rows: int = 4
    interfloor_blocking_rows: int = 4
    attic_blocking_rows: int = 4

    external_openings: list[OpeningIn] = Field(default_factory=list)
    internal_walls: list[InternalWallIn] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_logic(self):
        if not self.has_ground_overlap and not self.has_attic_overlap:
            raise ValueError("At least one overlap must be defined")

        if self.length < self.width:
            raise ValueError("Length must be >= width")

        if self.total_floors > 3:
            raise ValueError("Total_floors must be <= 3")

        if self.external_openings:
            for op in self.external_openings:
                if op.height >= self.wall_height:
                    raise ValueError("Opening height must be < wall_height")
                if op.width >= self.length:
                    raise ValueError("Opening width must be < wall length")

        if self.internal_walls:
            for iw in self.internal_walls:
                if iw.length >= self.length:
                    raise ValueError("Internal_walls length must be < wall length")
                if iw.openings:
                    for op in iw.openings:
                        if op.height >= self.wall_height:
                            raise ValueError("Opening height must be < wall_height")
                        if op.width >= iw.length:
                            raise ValueError("Opening width must be < wall length")

        return self
