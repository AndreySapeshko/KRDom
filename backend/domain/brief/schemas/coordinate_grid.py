from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field

# ----------------------------
# Coordinate system
# ----------------------------


class CoordinateSystem(BaseModel):
    units: Literal["meters"] = "meters"
    origin: Literal["bottom_left"] = "bottom_left"
    axis: str = "x-right, y-up"


# ----------------------------
# Axes grid
# ----------------------------


class AxisX(BaseModel):
    id: str  # "1", "2", ...
    x: float


class AxisY(BaseModel):
    id: str  # "A", "B", ...
    y: float


class GridAxes(BaseModel):
    x: List[AxisX] = Field(default_factory=list)
    y: List[AxisY] = Field(default_factory=list)


class AxisNaming(BaseModel):
    x_next: int = 1
    y_next: str = "A"
