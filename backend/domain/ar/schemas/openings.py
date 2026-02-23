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
    swing_direction: Optional[Literal["left", "right"]] = None
    swing_angle_deg: Optional[float] = Field(default=90, ge=30, le=120)

    @model_validator(mode="after")
    def validate_params_by_type(self):
        """
        Door must have hinge + swing defined.
        """
        if self.type in ("door", "interior_door"):
            if self.hinge_side is None:
                # raise ValueError(f"Door {self.id} must define hinge_side=start|end")
                self.hinge_side = "start"
            if self.swing_direction is None:
                # raise ValueError(f"Door {self.id} must define swing_direction=in|out")
                self.swing_direction = "right"
            if self.sill_height_m:
                self.sill_height_m = None

        # --- portal ---
        if self.type == "portal":
            self.sill_height_m = None
            self.swing_angle_deg = None
            self.hinge_side = None
            self.swing_direction = None

        if self.type == "window":
            self.swing_angle_deg = None
            self.hinge_side = None
            self.swing_direction = None
            if self.sill_height_m is None:
                self.sill_height_m = 0.8

        return self
