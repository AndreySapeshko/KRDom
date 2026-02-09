from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.v1.schemas.calc_input import CalcInputV1
from backend.core.models.calc_result import CalcResultV1
from backend.db.models.pdf_token import PdfToken
from backend.db.models.user import User
from backend.pdf.builder import build_pdf_report_v1
from backend.pdf.renderer import render_pdf_v1
from backend.repositories.calculation import CalculationRepository
from backend.repositories.token import TokenRepository


class ExportService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def export_pdf_v1(
        self,
        calc_id: UUID,
        user: User,
    ) -> bytes | None:
        repo = CalculationRepository(self.session)

        calc = await repo.get_calculation_by_id(calc_id)
        if not calc:
            raise HTTPException(404, "Calculation not found")
        if calc.user_id != user.id:
            raise HTTPException(403, "Forbidden")
        calc_result = CalcResultV1(**calc.calc_result)

        # здесь можно:
        # - проверить владельца
        # - проверить статус расчёта
        # - проверить лимиты

        report = await build_pdf_report_v1(
            calc_version=calc.calc_version,
            calc_input=CalcInputV1(**calc.input_data),
            calc_result=calc_result,
            session=self.session,
            username=user.username,
        )

        return render_pdf_v1(report)

    async def get_token(self, calc_id: UUID, user: User) -> str:
        repo = TokenRepository(self.session)
        return (await repo.get_or_create_pdf_token(calc_id, user)).token

    async def get_pdf_token(self, token: str) -> PdfToken | None:
        repo = TokenRepository(self.session)
        return await repo.get_pdf_token(token)

    async def delete_pdf_token(self, pdf_token: PdfToken):
        repo = TokenRepository(self.session)
        await repo.delete(pdf_token.token)
