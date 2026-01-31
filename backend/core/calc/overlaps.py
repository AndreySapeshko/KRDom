from backend.core.calc.context import CalcContext
from backend.core.calc.utils import _calc_single_overlap
from backend.core.models.calc_item import CalcItem
from backend.core.models.enums import GroupEnum


def calc_overlaps(ctx: CalcContext) -> list[CalcItem]:
    items: list[CalcItem] = []

    # ground overlap
    if ctx.has_ground_overlap:
        items += _calc_single_overlap(
            group=GroupEnum.GROUND_OVERLAP,
            section=ctx.ground_overlap_section,
            blocking_rows=ctx.ground_blocking_rows,
            ctx=ctx,
        )

    # interfloor overlap
    if ctx.has_interfloor_overlap:
        items += _calc_single_overlap(
            group=GroupEnum.INTERFLOOR_OVERLAP,
            section=ctx.interfloor_overlap_section,
            blocking_rows=ctx.interfloor_blocking_rows,
            ctx=ctx,
        )

    # attic overlap
    if ctx.has_attic_overlap:
        items += _calc_single_overlap(
            group=GroupEnum.ATTIC_OVERLAP,
            section=ctx.attic_overlap_section,
            blocking_rows=ctx.attic_blocking_rows,
            ctx=ctx,
        )

    return items
