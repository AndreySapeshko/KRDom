from datetime import datetime

from pydantic import BaseModel


class PdfMaterialRow(BaseModel):
    section_id: str
    height_mm: int
    width_mm: int
    length_mm: int | None
    kind: str  # standard / planed / lath


class PdfGroupSectionRow(BaseModel):
    section_id: str

    lm: float
    lm_with_waste: float
    volume_m3: float


class PdfGroupBlock(BaseModel):
    group: str
    sections: list[PdfGroupSectionRow]


class PdfSectionTotal(BaseModel):
    section_id: str

    lm: float
    lm_with_waste: float
    volume_m3: float


class PdfSummary(BaseModel):
    volume_without_waste_m3: float
    volume_with_waste_m3: float
    waste_volume_m3: float
    waste_factor: str
    total_usable_area_of_board: float
    total_volume_insulation: float

    total_roof_area: float
    total_overhang_area: float
    total_roof_perimeter: float
    total_length_ridge: float
    total_length_gable: float
    total_length_eave: float

    total_external_walls_area: float
    total_internal_walls_area: float
    total_ceilings_area: float
    total_floors_area: float


class PdfHeader(BaseModel):
    title: str = "KRDom — Расчёт пиломатериалов"
    generated_at: datetime
    username: str


class PdfReportV1(BaseModel):
    header: PdfHeader
    summary: PdfSummary
    section_totals: list[PdfSectionTotal]
    groups: list[PdfGroupBlock]
    materials: list[PdfMaterialRow]
