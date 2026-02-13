from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator

from backend.domain.ar.validators.geometry import Point2D, distance


class Wall(BaseModel):
    id: str  # EW1, IW1...
    kind: Literal["external", "internal"]

    from_point: Point2D
    to_point: Point2D

    thickness_m: float = Field(..., gt=0.05, lt=1.0)

    bearing: bool = False
    orientation: Optional[str] = None

    def length(self) -> float:
        return distance(self.from_point, self.to_point)

    @model_validator(mode="after")
    def validate_length(self):
        if self.length() < 0.3:
            raise ValueError(f"Wall {self.id} is too short (<0.3m)")
        return self
