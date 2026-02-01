from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.auth.dependencies import get_current_admin
from backend.api.auth.telegram_auth.dependencies import get_current_user
from backend.api.v1.schemas.material import MaterialIn, MaterialOut
from backend.db import User
from backend.db.session import get_session
from backend.repositories.material import MaterialRepository

router = APIRouter()


@router.post("", response_model=MaterialOut)
async def append_material(
    data: MaterialIn,
    current_user: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
):
    repo = MaterialRepository(session)

    material = await repo.get_or_create(data)

    return material


@router.post("/bulk", response_model=list[MaterialOut])
async def append_material_list(
    data: list[MaterialIn],
    current_user: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
):
    repo = MaterialRepository(session)
    materials = await repo.bulk_create(data)

    return materials


@router.put("/{id}", response_model=bool)
async def activate_deactivate_material(
    id: UUID,
    is_active: bool,
    current_user: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
) -> bool:
    repo = MaterialRepository(session)

    is_successful = await repo.activate_deactivate(id, is_active)

    return is_successful


@router.get("/all", response_model=list[MaterialOut])
async def get_all_materials(
    current_user: User = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
):
    repo = MaterialRepository(session)
    materials = await repo.all_list()

    return materials


@router.get("", response_model=list[MaterialOut])
async def get_materials(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    repo = MaterialRepository(session)
    materials = await repo.active_list()

    return materials


@router.get("/{section_id}", response_model=Optional[MaterialOut])
async def get_material_by_section_id(
    section_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    repo = MaterialRepository(session)
    material = await repo.get_by_section_id(section_id)

    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")

    return material
