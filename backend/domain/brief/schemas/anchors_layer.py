from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from backend.domain.brief.schemas.required_elements import RequiredElementV1


class AnchorsLayer(BaseModel):
    required_elements: List[RequiredElementV1] = Field(default_factory=list)
