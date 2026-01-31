from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MaterialIn(BaseModel):
    section_id: str
    width_mm: int
    height_mm: int
    length_mm: int | None = None
    kind: str


class MaterialOut(MaterialIn):
    id: UUID
    section_id: str
    width_mm: int
    height_mm: int
    length_mm: int
    kind: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
