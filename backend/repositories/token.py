import secrets
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import Calculation
from backend.db.models.pdf_token import PdfToken
from backend.db.models.user import User


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_pdf_token(self, calc_id: UUID, user: User) -> PdfToken:
        calc = await self.session.get(Calculation, calc_id)
        if not calc:
            raise HTTPException(404, "Calculation not found")
        if calc.user_id != user.id:
            raise HTTPException(403, "Forbidden")

        stmt = select(PdfToken).where(PdfToken.calc_id == calc_id, PdfToken.username == user.username)
        pdf_token = (await self.session.execute(stmt)).scalar_one_or_none()
        expires = datetime.utcnow() + timedelta(minutes=5)

        if pdf_token:
            await self.session.delete(pdf_token)
            await self.session.flush()

        token = secrets.token_urlsafe(32)
        pdf_token = PdfToken(
            token=token,
            calc_id=calc_id,
            username=user.username,
            expires_at=expires,
        )
        self.session.add(pdf_token)
        await self.session.commit()
        return pdf_token

    async def get_pdf_token(self, token: str) -> PdfToken | None:
        return await self.session.get(PdfToken, token)

    async def delete(self, token: str):
        stmt = delete(PdfToken).where(PdfToken.token == token)
        await self.session.execute(stmt)
        await self.session.commit()
