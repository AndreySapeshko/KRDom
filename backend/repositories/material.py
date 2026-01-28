from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.v1.schemas.material import MaterialIn
from backend.db.models.material import Material


class MaterialRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, data: MaterialIn) -> Material:
        stmt = select(Material).where(
            Material.section_id == data.section_id,
            Material.width_mm == data.width_mm,
            Material.height_mm == data.height_mm,
            Material.length_mm == data.length_mm,
            Material.kind == data.kind,
        )
        material = (await self.session.execute(stmt)).scalar_one_or_none()
        if material:
            return material

        material = Material(**data.dict())
        self.session.add(material)
        await self.session.commit()
        await self.session.refresh(material)
        return material

    async def bulk_create(self, items: list[MaterialIn]) -> list[Material]:
        materials = []
        for item in items:
            material = await self.get_or_create(item)
            materials.append(material)
        return materials

    async def get_by_section_id(self, section_id: str) -> Material | None:
        stmt = select(Material).where(Material.section_id == section_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def all_list(self) -> list[Material]:
        result = await self.session.execute(select(Material))
        return result.scalars().all()

    async def active_list(self) -> list[Material]:
        result = await self.session.execute(select(Material).where(Material.is_active.is_(True)))
        return result.scalars().all()

    async def activate_deactivate(self, material_id, is_active) -> bool:
        stmt = select(Material).where(Material.id == material_id)
        material = (await self.session.execute(stmt)).scalar_one_or_none()
        if material is None:
            return False
        material.is_active = is_active
        self.session.add(material)
        await self.session.commit()
        return True
