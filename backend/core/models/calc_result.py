from pydantic import BaseModel

from .calc_item import CalcItem
from .summary import CalcSummary
from .totals import GroupTotal, SectionTotal


class CalcResultV1(BaseModel):
    items: list[CalcItem]
    totals_by_section: list[SectionTotal]
    totals_by_group: list[GroupTotal]
    summary: CalcSummary
