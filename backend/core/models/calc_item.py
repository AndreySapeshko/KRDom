from pydantic import BaseModel

from .enums import ElementEnum, GroupEnum


class CalcItem(BaseModel):
    group: GroupEnum
    element: ElementEnum
    section_id: str

    lm: float
    lm_with_waste: float
    volume_m3: float
