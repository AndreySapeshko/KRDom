from pydantic import BaseModel

from backend.api.v1.schemas.calc_input import OpeningIn, OpeningTypes

from .calc_item import CalcItem
from .summary import CalcSummary
from .totals import GroupTotal, SectionTotal


class CalcResultV1(BaseModel):
    items: list[CalcItem]
    totals_by_section: list[SectionTotal]
    totals_by_group: list[GroupTotal]
    external_openings: dict[OpeningTypes, list[OpeningIn]]
    internal_openings: dict[OpeningTypes, list[OpeningIn]]
    summary: CalcSummary
