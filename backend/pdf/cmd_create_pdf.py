from datetime import datetime

from backend.api.v1.schemas.material import MaterialIn
from backend.core.aggregators.builder import build_calc_result
from backend.core.models.calc_result import CalcResultV1
from backend.pdf.renderer import render_pdf_v1
from backend.pdf.schemas.calc_result import (
    PdfGroupBlock,
    PdfGroupSectionRow,
    PdfHeader,
    PdfMaterialRow,
    PdfReportV1,
    PdfSectionTotal,
    PdfSummary,
)
from backend.tests.core.test_golden_calc import load_items

MATERIAL_SECTIONS = [
    MaterialIn(section_id="BOARD_50x150x6", width_mm=50, height_mm=150, length_mm=6000, kind="GOST 8683 1-2 grade"),
    MaterialIn(section_id="BOARD_50x200x6", width_mm=50, height_mm=200, length_mm=6000, kind="GOST 8683 1-2 grade"),
    MaterialIn(section_id="BOARD_25x100x6", width_mm=25, height_mm=100, length_mm=6000, kind="GOST 8683 1-2 grade"),
]


def sync_build_pdf_report_v1(
    calc_result: CalcResultV1,
    material_sections: list,
    username: str | None = None,
) -> PdfReportV1:
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
        section_totals=[PdfSectionTotal(**s.model_dump()) for s in calc_result.totals_by_section],
        groups=[
            PdfGroupBlock(
                group=g.group,
                sections=[PdfGroupSectionRow(**s.model_dump()) for s in g.totals_by_section],
            )
            for g in calc_result.totals_by_group
        ],
        materials=[
            PdfMaterialRow(
                section_id=m.section_id,
                width_mm=m.width_mm,
                height_mm=m.height_mm,
                length_mm=m.length_mm,
                kind=m.kind,
            )
            for m in material_sections
        ],
    )


def main():
    items = load_items("golden_2")
    calc_result = build_calc_result(items, waste_factor=1.1)
    pdf_report = sync_build_pdf_report_v1(calc_result, MATERIAL_SECTIONS, "Tester")

    pdf_bytes = render_pdf_v1(pdf_report)

    with open("test_report.pdf", "wb") as f:
        f.write(pdf_bytes)


main()
