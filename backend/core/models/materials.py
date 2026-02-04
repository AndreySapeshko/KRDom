from pydantic import BaseModel


class MaterialSection(BaseModel):
    section_id: str
    width_mm: int
    height_mm: int
    kind: str  # standard / planed / lath
    length_mm: int | None
