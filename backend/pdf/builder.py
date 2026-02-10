from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.v1.schemas.calc_input import CalcInputV1
from backend.core.aggregators.grouped_openings import get_dict_grouped_openings
from backend.core.aggregators.internal_opening import get_grouped_internal_openings
from backend.core.models.calc_result import CalcResultV1
from backend.pdf.schemas.calc_result import (
    PdfGroupBlock,
    PdfGroupSectionRow,
    PdfHeader,
    PdfMaterialRow,
    PdfReportV1,
    PdfSectionTotal,
    PdfSummary,
    PdfOpening,
)
from backend.pdf.translator import GROUP_RU, SECTION_RU, OPENING_GROUP_RU, OPENING_TYPE_RU
from backend.repositories.material import MaterialRepository


async def build_pdf_report_v1(
    calc_version: str,
    calc_input: CalcInputV1,
    calc_result: CalcResultV1,
    session: AsyncSession,
    username: str | None = None,
) -> PdfReportV1:
    repo = MaterialRepository(session)
    materials = await repo.active_list()
    section_ids = [section.section_id for section in calc_result.totals_by_section]
    material_sections = [material for material in materials if material.section_id in section_ids]
    external_openings = get_dict_grouped_openings(calc_input.external_openings)
    internal_openings = get_grouped_internal_openings(calc_input.internal_walls)

    return PdfReportV1(
        header=PdfHeader(
            calc_version=calc_version,
            generated_at=datetime.utcnow(),
            username=username if username else "unknown",
        ),
        summary=PdfSummary(
            volume_without_waste_m3=calc_result.summary.volume_total_without_waste_m3,
            volume_with_waste_m3=calc_result.summary.volume_total_m3,
            waste_volume_m3=calc_result.summary.volume_waste_m3,
            waste_factor=f"{int((calc_result.summary.waste_factor - 1) * 100)} %",
            total_usable_area_of_board=calc_result.summary.total_usable_area_of_board,
            total_volume_insulation=calc_result.summary.total_volume_insulation,
            total_roof_area=calc_result.summary.total_roof_area,
            total_overhang_area=calc_result.summary.total_overhang_area,
            total_roof_perimeter=calc_result.summary.total_roof_perimeter,
            total_length_ridge=calc_result.summary.total_length_ridge,
            total_length_gable=calc_result.summary.total_length_gable,
            total_length_eave=calc_result.summary.total_length_eave,
            total_external_walls_area=calc_result.summary.total_external_walls_area,
            total_internal_walls_area=calc_result.summary.total_internal_walls_area,
            total_ceilings_area=calc_result.summary.total_ceilings_area,
            total_floors_area=calc_result.summary.total_floors_area,
            width_building=calc_result.summary.width_building,
            length_building=calc_result.summary.length_building,
            height_building=calc_result.summary.height_building,
            roof_pitch_deg=calc_result.summary.roof_pitch_deg,
        ),
        section_totals=[
            PdfSectionTotal(
                section_id=SECTION_RU.get(s.section_id, s.section_id),
                lm=s.lm,
                lm_with_waste=s.lm_with_waste,
                volume_m3=s.volume_m3,
            )
            for s in calc_result.totals_by_section
        ],
        groups=[
            PdfGroupBlock(
                group=GROUP_RU.get(g.group, g.group),
                sections=[
                    PdfGroupSectionRow(
                        section_id=SECTION_RU.get(s.section_id, s.section_id),
                        lm=s.lm,
                        lm_with_waste=s.lm_with_waste,
                        volume_m3=s.volume_m3,
                    )
                    for s in g.totals_by_section
                ],
            )
            for g in calc_result.totals_by_group
        ],
        materials=[
            PdfMaterialRow(
                section_id=SECTION_RU.get(m.section_id, m.section_id),
                width_mm=m.width_mm,
                height_mm=m.height_mm,
                length_mm=m.length_mm,
                kind=m.kind,
            )
            for m in material_sections
        ],
        external_openings={
            OPENING_GROUP_RU.get(k, k): [
                PdfOpening(
                    type=OPENING_TYPE_RU.get(op.type, op.type), width=op.width, height=op.height, quantity=op.quantity
                )
                for op in v
            ]
            for k, v in external_openings.items()
        },
        internal_openings={
            OPENING_GROUP_RU.get(k, k): [
                PdfOpening(
                    type=OPENING_TYPE_RU.get(op.type, op.type), width=op.width, height=op.height, quantity=op.quantity
                )
                for op in v
            ]
            for k, v in internal_openings.items()
        },
    )
