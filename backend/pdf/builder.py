from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.models.calc_result import CalcResultV1
from backend.pdf.schemas.calc_result import (
    PdfGroupBlock,
    PdfGroupSectionRow,
    PdfHeader,
    PdfMaterialRow,
    PdfReportV1,
    PdfSectionTotal,
    PdfSummary,
)
from backend.repositories.material import MaterialRepository
from backend.pdf.translator import ELEMENT_RU, GROUP_RU, SECTION_RU


async def build_pdf_report_v1(
    calc_result: CalcResultV1,
    session: AsyncSession,
    username: str | None = None,
) -> PdfReportV1:
    repo = MaterialRepository(session)
    materials = await repo.active_list()
    section_ids = [section.section_id for section in calc_result.totals_by_section]
    material_sections = [material for material in materials if material.section_id in section_ids]

    return PdfReportV1(
        header=PdfHeader(
            generated_at=datetime.utcnow(),
            username=username,
        ),
        summary=PdfSummary(
            volume_without_waste_m3=calc_result.summary.volume_total_without_waste_m3,
            volume_with_waste_m3=calc_result.summary.volume_total_m3,
            waste_volume_m3=calc_result.summary.volume_waste_m3,
            waste_factor=f"{int((calc_result.summary.waste_factor - 1) * 100)} %",
        ),
        section_totals=[
            PdfSectionTotal(
                section_id=SECTION_RU.get(s.section_id, s.section_id),
                lm=s.lm,
                lm_with_waste=s.lm_with_waste,
                volume_m3=s.volume_m3
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
                        volume_m3=s.volume_m3
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
    )
