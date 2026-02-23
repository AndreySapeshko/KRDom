from __future__ import annotations

from pydantic import BaseModel


class InteriorDoor(BaseModel):
    id: str
    from_room: str
    to_room: str
    position: list[float]
    width_m: float


class ExternalDoor(BaseModel):
    id: str
    to_room: str
    position: list[float]
    width_m: float
