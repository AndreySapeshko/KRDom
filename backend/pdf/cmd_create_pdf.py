from datetime import datetime

from backend.api.v1.schemas.calc_input import CalcInputV1
from backend.api.v1.schemas.material import MaterialIn
from backend.core.aggregators.builder import build_calc_result
from backend.core.aggregators.grouped_openings import get_dict_grouped_openings
from backend.core.aggregators.internal_opening import get_grouped_internal_openings
from backend.core.calc.context import CalcContext, InternalWall, Opening
from backend.core.models.calc_result import CalcResultV1
from backend.core.models.enums import OpeningTypes
from backend.db.models.material import Material
from backend.pdf.input_data import INPUT_DATA
from backend.pdf.renderer import render_pdf_v1
from backend.pdf.schemas.calc_result import (
    PdfGroupBlock,
    PdfGroupSectionRow,
    PdfHeader,
    PdfMaterialRow,
    PdfOpening,
    PdfReportV1,
    PdfSectionTotal,
    PdfSummary,
)
from backend.pdf.translator import GROUP_RU, OPENING_GROUP_RU, OPENING_TYPE_RU, SECTION_RU
from backend.tests.core.test_golden_calc import load_items

MATERIAL_SECTIONS = [
    MaterialIn(section_id="BOARD_50x150x6", width_mm=50, height_mm=150, length_mm=6000, kind="GOST 8683 1-2 grade"),
    MaterialIn(section_id="BOARD_50x200x6", width_mm=50, height_mm=200, length_mm=6000, kind="GOST 8683 1-2 grade"),
    MaterialIn(section_id="BOARD_25x100x6", width_mm=25, height_mm=100, length_mm=6000, kind="GOST 8683 1-2 grade"),
]

context = CalcContext(
    length=8.0,
    width=6.0,
    wall_height=2.7,
    total_floors=1,
    is_fronton_short=True,
    stud_spacing=0.63,
    joist_spacing=0.63,
    rafter_spacing=0.63,
    wall_section=Material(
        section_id="BOARD_50x150", width_mm=150, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
    ),
    ground_overlap_section=Material(
        section_id="BOARD_50x200", width_mm=200, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
    ),
    interfloor_overlap_section=Material(
        section_id="BOARD_50x200", width_mm=200, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
    ),
    attic_overlap_section=Material(
        section_id="BOARD_50x150", width_mm=150, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
    ),
    roof_section=Material(
        section_id="BOARD_50x200", width_mm=200, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
    ),
    lath_section=Material(
        section_id="BOARD_25x100", width_mm=100, height_mm=25, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
    ),
    counter_lath_section=Material(
        section_id="BAR_50x50", width_mm=50, height_mm=50, kind="ГОСТ 8683-83, 1-2 сорт", length_mm=6000
    ),
    waste_factor=1.1,
    roof_pitch_deg=35.0,
    eave_overhang=0.6,
    gable_overhang=0.6,
    lath_step=0.35,
    has_ground_overlap=True,
    has_interfloor_overlap=False,
    has_attic_overlap=True,
    ground_blocking_rows=4,
    interfloor_blocking_rows=4,
    attic_blocking_rows=4,
    external_openings=[
        Opening(type=OpeningTypes.WINDOW, height=1.2, width=1.4, quantity=6),
        Opening(type=OpeningTypes.DOOR, height=2.1, width=0.9, quantity=1),
    ],
    internal_walls=[
        InternalWall(length=5.7, openings=[Opening(type=OpeningTypes.DOOR, height=2.1, width=0.9, quantity=2)]),
        InternalWall(length=3.78, openings=[Opening(type=OpeningTypes.DOOR, height=2.1, width=0.9, quantity=1)]),
    ],
)


def sync_build_pdf_report_v1(
    calc_result: CalcResultV1,
    input_data: CalcInputV1,
    material_sections: list,
    username: str | None = None,
) -> PdfReportV1:
    external_openings = get_dict_grouped_openings(input_data.external_openings)
    internal_openings = get_grouped_internal_openings(input_data.internal_walls)
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
                section_id=SECTION_RU.get(s.section_id.strip(), s.section_id),
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
                        section_id=SECTION_RU.get(s.section_id.strip(), "s.section_id"),
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


def main():
    items = load_items("golden_2")
    calc_result = build_calc_result(items, INPUT_DATA, ctx=context)
    pdf_report = sync_build_pdf_report_v1(calc_result, INPUT_DATA, MATERIAL_SECTIONS, "Tester")

    pdf_bytes = render_pdf_v1(pdf_report)

    with open("test_report.pdf", "wb") as f:
        f.write(pdf_bytes)


main()
