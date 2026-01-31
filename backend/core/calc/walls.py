from backend.core.calc.context import CalcContext
from backend.core.calc.utils import (
    _calc_external_walls,
    _calc_frame_opening,
    _calc_internal_opening,
    _calc_internal_plates,
    _calc_internal_walls,
    _calc_wall_plates,
)
from backend.core.models.calc_item import CalcItem
from backend.core.models.enums import ElementEnum, GroupEnum


def calc_walls(ctx: CalcContext) -> list[CalcItem]:
    items: list[CalcItem] = []

    items.append(_calc_external_walls(GroupEnum.EXTERNAL_WALLS, ctx))

    items.append(_calc_wall_plates(GroupEnum.EXTERNAL_WALLS, ElementEnum.PLATES_BOTTOM, ctx))

    items.append(_calc_wall_plates(GroupEnum.EXTERNAL_WALLS, ElementEnum.PLATES_TOP, ctx))

    items.append(_calc_frame_opening(GroupEnum.EXTERNAL_WALLS, ctx))

    items.append(_calc_internal_walls(GroupEnum.INTERNAL_WALLS, ctx))

    items.append(_calc_internal_plates(GroupEnum.INTERNAL_WALLS, ElementEnum.PLATES_TOP, ctx))

    items.append(_calc_internal_plates(GroupEnum.INTERNAL_WALLS, ElementEnum.PLATES_BOTTOM, ctx))

    items.append(_calc_internal_opening(GroupEnum.INTERNAL_WALLS, ctx))

    return items
