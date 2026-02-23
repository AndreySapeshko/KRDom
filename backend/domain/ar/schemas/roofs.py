from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Roof(BaseModel):
    type: Literal["gable", "hip", "multi_gable"]
    pitch_deg: float = Field(..., ge=5, le=60)

    eave_overhang_m: float = Field(default=0.6, ge=0)
    gable_overhang_m: float = Field(default=0.6, ge=0)
