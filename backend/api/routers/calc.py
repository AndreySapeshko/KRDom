from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.auth.telegram_auth.dependencies import get_current_user
from backend.api.v1.schemas.calc_input import CalcInputV1
from backend.core.services.calculation_service import CalculationService
from backend.db import User
from backend.db.session import get_session

router = APIRouter()


@router.post("")
async def calculate(
    data: CalcInputV1,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = CalculationService(session)

    calc = await service.calculate_and_save(
        input_data=data,
        user_id=current_user.id,
        source="telegram",
    )

    return calc
