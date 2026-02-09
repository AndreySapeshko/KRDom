from backend.core.models.calc_item import CalcItem
from backend.core.models.calc_result import CalcResultV1

from ...api.v1.schemas.calc_input import CalcInputV1
from ..calc.context import CalcContext
from .by_group import aggregate_by_group
from .by_section import aggregate_by_section
from .grouped_openings import get_dict_grouped_openings
from .internal_opening import get_grouped_internal_openings
from .summary import build_summary


def build_calc_result(items: list[CalcItem], input_data: CalcInputV1, ctx: CalcContext) -> CalcResultV1:
    totals_by_section = aggregate_by_section(items)
    summary = build_summary(items, input_data.waste_factor, ctx, totals_by_section)
    return CalcResultV1(
        items=items,
        totals_by_section=totals_by_section,
        totals_by_group=aggregate_by_group(items),
        external_openings=get_dict_grouped_openings(input_data.external_openings),
        internal_openings=get_grouped_internal_openings(input_data.internal_walls),
        summary=summary,
    )
