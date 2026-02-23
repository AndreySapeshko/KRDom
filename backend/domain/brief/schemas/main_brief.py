from __future__ import annotations

import json
from pathlib import Path
from typing import List, Literal

from pydantic import BaseModel, Field, model_validator

from backend.domain.ar.schemas.openings import Opening
from backend.domain.brief.schemas.anchors_layer import AnchorsLayer
from backend.domain.brief.schemas.coordinate_grid import AxisNaming, CoordinateSystem, GridAxes
from backend.domain.brief.schemas.intent_layer import IntentLayer
from backend.domain.brief.schemas.polygon import PolygonFootprint

BASE_DIR = Path(__file__).parent


class WallSpec(BaseModel):
    structural_type: str = "frame"
    thickness_m: float = Field(..., gt=0.05, lt=1.0)


class BuildingInfo(BaseModel):
    footprint: PolygonFootprint
    floors: int = Field(..., ge=1)
    wall_height: float = Field(..., gt=0)
    wall_spec: WallSpec


class ProjectBriefV1(BaseModel):
    version: Literal["1.0"] = "1.0"

    coordinate_system: CoordinateSystem = Field(default_factory=CoordinateSystem)

    building: BuildingInfo
    grid_axes: GridAxes = Field(default_factory=GridAxes)
    axis_naming: AxisNaming = Field(default_factory=AxisNaming)

    intent: IntentLayer = Field(default_factory=IntentLayer)
    anchors: AnchorsLayer = Field(default_factory=AnchorsLayer)

    assumptions: List[str] = Field(default_factory=list)

    # ----------------------------
    # Global validation
    # ----------------------------

    @model_validator(mode="after")
    def validate_anchors(self):
        """
        Проверяем, что anchors ссылаются на существующие стены.
        Пока стены вычисляются из polygon сегментов:
        W1..Wn = количество сегментов.
        """

        pts = self.building.footprint.points
        wall_count = len(pts)

        # Генерируем допустимые wall_id
        valid_wall_ids = {f"EW{i + 1}" for i in range(wall_count)}

        # Проверка fixed openings
        for element in self.anchors.required_elements:
            if isinstance(element.spec, Opening):
                if element.spec.wall_id not in valid_wall_ids:
                    raise ValueError(
                        f"Anchor opening references unknown wall_id={element.spec.wall_id}. "
                        f"Valid: {sorted(valid_wall_ids)}"
                    )

        return self

    @classmethod
    def example(cls) -> "ProjectBriefV1":
        with open(BASE_DIR / "ProjectBriefV1.json", "r", encoding="utf-8") as f:
            brief = json.load(f)
        return cls(**brief)
