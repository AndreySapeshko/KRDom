from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from backend.domain.ar.schemas.footprint import BuildingGeometry
from backend.domain.ar.schemas.meta_and_rules import ConceptMeta, ModelingRules
from backend.domain.ar.schemas.openings import Opening
from backend.domain.ar.schemas.roofs import Roof
from backend.domain.ar.schemas.rooms import Room
from backend.domain.ar.schemas.walls import Wall


class ConceptOutputs(BaseModel):
    gross_building_area_m2: Optional[float] = None
    net_living_area_m2: Optional[float] = None


# ----------------------------
# Main Concept
# ----------------------------


class ArchitectureConceptV1(BaseModel):
    version: Literal["1.0"] = "1.0"

    meta: ConceptMeta
    modeling_rules: ModelingRules = Field(default_factory=ModelingRules)

    building_geometry: BuildingGeometry

    walls: List[Wall]
    openings: List[Opening]

    roof: Roof

    detected_rooms: Optional[List["Room"]] = None

    outputs: ConceptOutputs = Field(default_factory=ConceptOutputs)

    assumptions: List[str] = Field(default_factory=list)

    # ----------------------------
    # Global validation
    # ----------------------------

    @model_validator(mode="after")
    def validate_references(self):
        wall_ids = {w.id for w in self.walls}

        # Openings must reference existing walls
        for op in self.openings:
            if op.wall_id not in wall_ids:
                raise ValueError(f"Opening {op.id} references unknown wall_id={op.wall_id}")

        return self

    @model_validator(mode="after")
    def validate_opening_positions(self):
        """
        Проверяем что offset + width не выходят за длину стены.
        """
        wall_map = {w.id: w for w in self.walls}

        for op in self.openings:
            wall = wall_map[op.wall_id]
            wall_len = wall.length()

            if op.offset_m + op.width_m > wall_len:
                raise ValueError(
                    f"Opening {op.id} exceeds wall {wall.id}: "
                    f"offset+width={op.offset_m + op.width_m:.2f} > "
                    f"wall_length={wall_len:.2f}"
                )

        return self
