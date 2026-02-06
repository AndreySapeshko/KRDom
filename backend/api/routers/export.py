from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.auth.telegram_auth.dependencies import get_current_user
from backend.config import BASE_API_URL
from backend.core.services.export_service import ExportService
from backend.db import User
from backend.db.session import get_session

router = APIRouter()


@router.get("/{calc_id}/export/pdf-link")
async def export_pdf(
    calc_id: UUID, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    service = ExportService(session)
    token = await service.get_token(calc_id, current_user)

    return {"url": f"{BASE_API_URL}/calc/export/pdf?token={token}"}


@router.get("/export/pdf")
async def export_pdf_by_token(
    token: str = Query(...),
    session: AsyncSession = Depends(get_session),
):
    service = ExportService(session)
    pdf_token = await service.get_pdf_token(token)

    if not pdf_token:
        raise HTTPException(403, "Invalid token")

    if pdf_token.expires_at < datetime.utcnow():
        raise HTTPException(403, "Token expired")

    pdf_bytes = await service.export_pdf_v1(
        pdf_token.calc_id,
        pdf_token.username,
    )

    await service.delete_pdf_token(pdf_token)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "inline; filename=krdom.pdf",
            "Cache-Control": "no-store",
        },
    )
