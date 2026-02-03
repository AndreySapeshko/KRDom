from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from backend.pdf.schemas.calc_result import PdfReportV1

_env = Environment(
    loader=FileSystemLoader("backend/pdf/templates"),
    autoescape=True,
)

def render_pdf_v1(report: PdfReportV1) -> bytes:
    template = _env.get_template("report_v1.html")

    html = template.render(report=report)

    pdf_bytes = HTML(
        string=html,
        base_url="backend/pdf/templates",
    ).write_pdf()

    return pdf_bytes
