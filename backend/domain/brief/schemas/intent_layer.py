from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class RoomRequirement(BaseModel):
    type: str  # "living_room", "kitchen", ...
    min_area: float = Field(..., gt=0)
    count: Optional[int] = Field(default=1, ge=1)


class FeaturesIntent(BaseModel):
    terrace: bool = False
    panoramic_windows: bool = False


class RoofPreferences(BaseModel):
    allowed_types: List[str] = Field(default_factory=lambda: ["gable"])


class IntentLayer(BaseModel):
    rooms_required: List[RoomRequirement] = Field(default_factory=list)
    features: FeaturesIntent = Field(default_factory=FeaturesIntent)
    roof_preferences: RoofPreferences = Field(default_factory=RoofPreferences)
