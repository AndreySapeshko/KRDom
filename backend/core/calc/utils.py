from math import ceil, cos, floor, radians, tan

from backend.core.calc.context import CalcContext
from backend.core.models.calc_item import CalcItem
from backend.core.models.enums import ElementEnum, GroupEnum, OpeningTypes
from backend.core.models.materials import MaterialSection


def _calc_single_overlap(
    group: GroupEnum, section: MaterialSection, blocking_rows: int, ctx: CalcContext
) -> list[CalcItem]:
    spacing = ctx.joist_spacing
    length = ctx.length
    width = ctx.width

    if length >= width:
        overlap_length = length
        overlap_width = width
    else:
        overlap_length = width
        overlap_width = length

    lm_joists = ceil(overlap_length / spacing) * overlap_width
    lm_blocking = floor(overlap_length / spacing) * spacing * blocking_rows
    lm_rim = (overlap_length + overlap_width) * 2

    result = []
    result.append(
        CalcItem(
            group=group,
            element=ElementEnum.JOISTS,
            section_id=section.section_id,
            lm=lm_joists,
            lm_with_waste=lm_joists * ctx.waste_factor,
            volume_m3=lm_joists * section.width_m * section.height_m,
        )
    )
    result.append(
        CalcItem(
            group=group,
            element=ElementEnum.RIM,
            section_id=section.section_id,
            lm=lm_rim,
            lm_with_waste=lm_rim * ctx.waste_factor,
            volume_m3=lm_rim * section.width_m * section.height_m,
        )
    )
    result.append(
        CalcItem(
            group=group,
            element=ElementEnum.BLOCKING,
            section_id=section.section_id,
            lm=lm_blocking,
            lm_with_waste=lm_blocking * ctx.waste_factor,
            volume_m3=lm_blocking * section.width_m * section.height_m,
        )
    )
    return result


def _calc_external_walls(group: GroupEnum, ctx: CalcContext) -> CalcItem:
    # 1. базовые стойки наружных стен
    length = ctx.length
    width = ctx.width
    height = ctx.wall_height
    spacing = ctx.stud_spacing
    lm_studs = (ceil(length / spacing) + ceil(width / spacing)) * 2 * height * ctx.total_floors
    # фронтон
    f_length = width if ctx.is_fronton_short else length
    count_studs = floor(f_length / spacing)
    lm_studs += (f_length / 2 * tan(ctx.roof_pitch_deg) + 0.4) * count_studs
    return CalcItem(
        group=group,
        element=ElementEnum.STUDS,
        section_id=ctx.wall_section.section_id,
        lm=lm_studs,
        lm_with_waste=lm_studs * ctx.waste_factor,
        volume_m3=lm_studs * ctx.wall_section.width_m * ctx.wall_section.height_m,
    )


def _get_length_width_roof(ctx: CalcContext):
    length = ctx.length
    width = ctx.width
    eave_overhang = ctx.eave_overhang
    gable_overhang = ctx.gable_overhang
    roof_pitch = ctx.roof_pitch_deg

    roof_length = length if ctx.is_fronton_short else width
    roof_length += eave_overhang * 2
    front_length = width if ctx.is_fronton_short else length
    roof_width = (front_length / 2 + gable_overhang) / cos(radians(roof_pitch))

    return roof_length, roof_width


def _calc_wall_plates(group: GroupEnum, element: ElementEnum, ctx: CalcContext) -> CalcItem:
    # 2. обвязки
    length = ctx.length
    width = ctx.width
    lm_plates_bottom = (length + width) * 4
    return CalcItem(
        group=group,
        element=element,
        section_id=ctx.wall_section.section_id,
        lm=lm_plates_bottom,
        lm_with_waste=lm_plates_bottom * ctx.waste_factor,
        volume_m3=lm_plates_bottom * ctx.wall_section.width_m * ctx.wall_section.height_m,
    )


def _calc_frame_opening(group: GroupEnum, ctx: CalcContext) -> CalcItem:
    # 3. проёмы (king / jack / header / sill)
    spacing = ctx.stud_spacing
    lm_frame_op = 0
    for op in ctx.external_openings:
        op_width = op.width
        op_height = op.height
        lm_op_king = ceil(op_width / spacing) * spacing
        op_king_count = 2 if lm_op_king > 1.26 else 1
        op_king_count += 1 if op.type is OpeningTypes.WINDOW else 0
        subtract_stud = lm_op_king / spacing - 1
        lm_one_frame_op = lm_op_king * op_king_count + op_height * 2 - op_height * subtract_stud
        lm_frame_op += lm_one_frame_op * op.quantity

    return CalcItem(
        group=group,
        element=ElementEnum.OPENING_FRAME,
        section_id=ctx.wall_section.section_id,
        lm=lm_frame_op,
        lm_with_waste=lm_frame_op * ctx.waste_factor,
        volume_m3=lm_frame_op * ctx.wall_section.height_m * ctx.wall_section.width_m,
    )


def _calc_internal_walls(group: GroupEnum, ctx: CalcContext) -> CalcItem:
    # 4. внутренние стены (без позиционирования)
    height = ctx.wall_height
    spacing = ctx.stud_spacing
    lm_internal_studs = 0
    for iw in ctx.internal_walls:
        iw_length = iw.length
        lm_internal_studs += ceil(iw_length / spacing) * height

    return CalcItem(
        group=group,
        element=ElementEnum.STUDS,
        section_id=ctx.wall_section.section_id,
        lm=lm_internal_studs,
        lm_with_waste=lm_internal_studs * ctx.waste_factor,
        volume_m3=lm_internal_studs * ctx.wall_section.width_m * ctx.wall_section.height_m,
    )


def _calc_internal_plates(group: GroupEnum, element: ElementEnum, ctx: CalcContext) -> CalcItem:
    # 4. внутренние стены (без позиционирования)
    lm_plates = 0
    for iw in ctx.internal_walls:
        iw_length = iw.length
        lm_plates += iw_length * 2

    return CalcItem(
        group=group,
        element=element,
        section_id=ctx.wall_section.section_id,
        lm=lm_plates,
        lm_with_waste=lm_plates * ctx.waste_factor,
        volume_m3=lm_plates * ctx.wall_section.width_m * ctx.wall_section.height_m,
    )


def _calc_internal_opening(group: GroupEnum, ctx: CalcContext) -> CalcItem:
    # 4. внутренние стены (без позиционирования)
    spacing = ctx.stud_spacing
    lm_frame_op = 0
    for iw in ctx.internal_walls:
        for op in iw.openings:
            op_width = op.width
            op_height = op.height
            lm_op_king = ceil(op_width / spacing) * spacing
            op_king_count = 2 if lm_op_king > 1.26 else 1
            op_king_count += 1 if op.type is OpeningTypes.WINDOW else 0
            subtract_stud = lm_op_king / spacing - 1
            lm_one_frame_op = lm_op_king * op_king_count + op_height * 2 - op_height * subtract_stud
            lm_frame_op += lm_one_frame_op * op.quantity

    return CalcItem(
        group=group,
        element=ElementEnum.OPENING_FRAME,
        section_id=ctx.wall_section.section_id,
        lm=lm_frame_op,
        lm_with_waste=lm_frame_op * ctx.waste_factor,
        volume_m3=lm_frame_op * ctx.wall_section.height_m * ctx.wall_section.width_m,
    )
