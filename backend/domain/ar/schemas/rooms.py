from __future__ import annotations

from enum import Enum
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field


class RoomType(str, Enum):
    LIVING = "LIVING"
    KITCHEN = "KITCHEN"
    BEDROOM = "BEDROOM"
    BATHROOM = "BATHROOM"
    HALL = "HALL"
    UTILITY = "UTILITY"
    UNKNOWN = "UNKNOWN"


class Room(BaseModel):
    id: str

    label: Optional[str] = None

    type: RoomType = RoomType.UNKNOWN

    net_area_m2: float = Field(..., gt=0)

    centroid: Tuple[float, float]

    boundary_wall_ids: List[str]

    polygon: Optional[List[Tuple[float, float]]] = None
