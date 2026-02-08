from math import radians, tan

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.aggregators.rounding import round_lm, round_volume
from backend.core.calc.context import CalcContext, Opening
from backend.core.models.calc_item import CalcItem
from backend.core.models.enums import GroupEnum
from backend.repositories.material import MaterialRepository


def get_openings_area(openings: list[Opening]):
    total_openings_area = 0
    for op in openings:
        total_openings_area += op.height * op.width * op.quantity

    return round_lm(total_openings_area)


async def get_width_m_material_by_group(
    items: list[CalcItem], group: GroupEnum, session: AsyncSession
) -> float | None:
    repo = MaterialRepository(session)
    for item in items:
        if item.group == group:
            section = await repo.get_by_section_id(item.section_id)
            return round_volume(section.width_mm / 1000)
    return 0


def calc_walls_area(ctx: CalcContext) -> dict:
    height_ground_overlap = ctx.ground_overlap_section.width_mm / 1000
    height_interfloor_overlap = ctx.interfloor_overlap_section.width_mm / 1000
    height_attic_overlap = ctx.attic_overlap_section.width_mm / 1000
    wall_thickness = ctx.wall_section.width_mm / 1000

    height = round_lm(
        ctx.wall_height * ctx.total_floors
        + height_ground_overlap
        + height_attic_overlap
        + height_interfloor_overlap * (ctx.total_floors - 1)
    )
    external_length = ctx.length
    external_width = ctx.width
    internal_length = external_length - wall_thickness * 2
    internal_width = external_width - wall_thickness * 2
    fronton_length = ctx.width if ctx.is_fronton_short else ctx.length
    fronton_height = fronton_length / 2 * tan(radians(ctx.roof_pitch_deg))

    external_openings_area = get_openings_area(ctx.external_openings)
    internal_openings_area = 0
    internal_walls_area = 0
    for i_wall in ctx.internal_walls:
        internal_walls_area += i_wall.length * ctx.wall_height * 2
        internal_openings_area += get_openings_area(i_wall.openings)

    external_walls_area = round_lm(
        (external_length + external_width) * 2 * height + fronton_height * fronton_length - external_openings_area
    )

    internal_walls_area += round_lm(
        (internal_length + internal_width) * 2 * (ctx.total_floors * ctx.wall_height)
        + fronton_height * fronton_length
        - external_openings_area
        - internal_openings_area
    )

    return {
        "total_external_walls_area": round_lm(external_walls_area),
        "total_internal_walls_area": round_lm(internal_walls_area),
    }
