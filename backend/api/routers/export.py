import logging

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.auth.telegram_auth.dependencies import get_current_user
from backend.bot.send_file_to_chat import send_pdf_report
from backend.config import BASE_API_URL
from backend.core.services.export_service import ExportService
from backend.db import User
from backend.db.session import get_session

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{calc_id}/export/pdf-link")
async def export_pdf(
    calc_id: UUID, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    service = ExportService(session)
    token = await service.get_token(calc_id, current_user)

    return {"url": f"{BASE_API_URL}/calc/export/pdf?token={token}"}


@router.post("/{calc_id}/export/send-to-chat")
async def send_pdf_to_chat(
    calc_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if not current_user.telegram_id:
        raise HTTPException(400, "Вы не подключены к боту. Для начала отправьте боту: /start")

    service = ExportService(session)

    pdf_bytes = await service.export_pdf_v1(calc_id, current_user)

    try:
        await send_pdf_report(
            chat_id=current_user.telegram_id,
            pdf_bytes=pdf_bytes,
            filename=f"krdom_{calc_id}.pdf",
        )
    except Exception as e:
        logger.exception("Telegram send_document failed")
        raise HTTPException(500, f"Telegram send failed: {e}")

    return {"status": "sent"}
