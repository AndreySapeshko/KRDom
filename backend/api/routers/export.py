from uuid import UUID

from fastapi import Response
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.auth.telegram_auth.dependencies import get_current_user
from backend.core.services.export_service import ExportService
from backend.db import User
from backend.db.session import get_session

router = APIRouter()


@router.get("/{calc_id}/pdf")
async def export_pdf(
        calc_id: UUID,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)):
    service = ExportService(session)
    pdf_bytes = await service.export_pdf_v1(calc_id, current_user.username)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="krdom_{calc_id}.pdf"',
            "Cache-Control": "no-store",
        },
    )
