from pydantic import BaseModel


class SectionTotal(BaseModel):
    section_id: str
    lm: float
    lm_with_waste: float
    volume_m3: float


class GroupTotal(BaseModel):
    group: str
    totals_by_section: list[SectionTotal]
