from typing import List, Literal, Optional

from pydantic import BaseModel, Field, conlist

from backend.domain.ar.schemas.doors import ExternalDoor
from backend.domain.brief.schemas.polygon import PolygonFootprint

# ---------- Room Rect ----------

Rect = conlist(float, min_length=4, max_length=4)


class RoomPolygon(BaseModel):
    """
    One rectangular room definition.
    rect = [x1, y1, x2, y2]
    """

    id: str = Field(..., description="Stable room identifier, e.g. LIVING, BED1")
    role: str = Field(..., description="living_room, kitchen, bedroom, bathroom...")

    polygon: PolygonFootprint = Field(..., description="Room polygon: [[x1,y1], [x2,y2], ...] in meters")

    min_area: Optional[float] = Field(default=None, description="Optional requirement area")

    def area(self) -> float:
        points = self.polygon.points
        area = 0.0
        n = len(points)

        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            area += x1 * y2 - x2 * y1

        return abs(area) / 2.0


# ---------- Layout ----------


class DoorsList(BaseModel):
    external_doors: List[ExternalDoor] = Field(default_factory=list)
    interior_doors: List[ExternalDoor] = Field(default_factory=list)


class RoomLayoutV2(BaseModel):
    """
    Output of LLM: conceptual rectangular room layout.
    """

    version: Literal["1.0"] = "1.0"

    rooms: List[RoomPolygon]

    doors: DoorsList = Field(default_factory=list)

    connections: List[List[str]] = Field(default_factory=list)

    assumptions: List[str] = Field(default_factory=list)
