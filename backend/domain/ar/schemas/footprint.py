from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, model_validator

from backend.domain.ar.validators.geometry import Point2D, polygon_area


class Footprint(BaseModel):
    points: List[Point2D] = Field(..., min_length=3)

    @model_validator(mode="after")
    def validate_area(self):
        area = polygon_area(self.points)
        if area < 1.0:
            raise ValueError("Footprint area must be >= 1 m²")
        return self


class BuildingGeometry(BaseModel):
    footprint: Footprint
