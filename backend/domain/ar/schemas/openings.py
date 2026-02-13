from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class Opening(BaseModel):
    id: str  # WIN1, D1, ID1...

    type: Literal["window", "door", "interior_door", "portal"]

    wall_id: str

    offset_m: float = Field(..., ge=0)
    width_m: float = Field(..., gt=0)
    height_m: float = Field(..., gt=0)

    sill_height_m: Optional[float] = Field(default=None, ge=0)

    style: Optional[str] = None

    # ----------------------------
    # Door-specific parameters
    # ----------------------------

    hinge_side: Optional[Literal["start", "end"]] = None
    swing_direction: Optional[Literal["in", "out"]] = None
    swing_angle_deg: float = Field(default=90, ge=30, le=120)

    @model_validator(mode="after")
    def validate_door_params(self):
        """
        Door must have hinge + swing defined.
        """
        if self.type in ("door", "interior_door"):
            if self.hinge_side is None:
                raise ValueError(f"Door {self.id} must define hinge_side=start|end")
            if self.swing_direction is None:
                raise ValueError(f"Door {self.id} must define swing_direction=in|out")

        # --- portal ---
        if self.type == "portal":
            # portal не имеет swing
            if self.hinge_side is not None or self.swing_direction is not None:
                raise ValueError(f"Portal {self.id} must not define hinge/swing params")

            # portal всегда от пола → sill_height запрещён
            if self.sill_height_m not in (None, 0):
                raise ValueError(f"Portal {self.id} must not have sill_height_m")

        return self
