from typing import List, Literal, Optional

from pydantic import BaseModel, Field, conlist

# ---------- Room Rect ----------

Rect = conlist(float, min_length=4, max_length=4)


class RoomBox(BaseModel):
    """
    One rectangular room definition.
    rect = [x1, y1, x2, y2]
    """

    id: str = Field(..., description="Stable room identifier, e.g. LIVING, BED1")
    role: str = Field(..., description="living_room, kitchen, bedroom, bathroom...")

    rect: Rect = Field(..., description="Room rectangle: [x1,y1,x2,y2] in meters")

    min_area: Optional[float] = Field(default=None, description="Optional requirement area")

    def area(self) -> float:
        x1, y1, x2, y2 = self.rect
        return abs((x2 - x1) * (y2 - y1))


# ---------- Layout ----------


class RoomLayoutV1(BaseModel):
    """
    Output of LLM: conceptual rectangular room layout.
    """

    version: Literal["1.0"] = "1.0"

    rooms: List[RoomBox]

    assumptions: List[str] = Field(default_factory=list)
