from datetime import datetime

from pydantic import BaseModel

from backend.core.models.enums import GroupEnum


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
