from backend.core.models.calc_item import CalcItem
from backend.core.models.calc_result import CalcResultV1

from ..calc.context import CalcContext
from .by_group import aggregate_by_group
from .by_section import aggregate_by_section
from .summary import build_summary


def build_calc_result(items: list[CalcItem], waste_factor: float, ctx: CalcContext) -> CalcResultV1:
    totals_by_section = aggregate_by_section(items)
    summary = build_summary(items, waste_factor, ctx, totals_by_section)
    return CalcResultV1(
        items=items,
        totals_by_section=totals_by_section,
        totals_by_group=aggregate_by_group(items),
        summary=summary,
    )
