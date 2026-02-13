from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# ----------------------------
# Meta
# ----------------------------


class ConceptMeta(BaseModel):
    project_id: str
    stage: Literal["AR_CONCEPT"] = "AR_CONCEPT"
    iteration: int = Field(default=1, ge=1)


# ----------------------------
# Modeling rules
# ----------------------------


class ModelingRules(BaseModel):
    footprint_reference: Literal["wall_centerline"] = "wall_centerline"
    net_area_rule: Literal["inside_wall_faces"] = "inside_wall_faces"
