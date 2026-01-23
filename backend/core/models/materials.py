from pydantic import BaseModel


class MaterialSection(BaseModel):
    section_id: str
    width_m: float
    height_m: float
    kind: str  # standard / planed / lath
    length: str | None
