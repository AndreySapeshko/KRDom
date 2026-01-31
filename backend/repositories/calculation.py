from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.v1.schemas.calc_input import CalcInputV1
from backend.core.models.calc_result import CalcResultV1
from backend.core.models.planning import PlanningRequirementsV1
from backend.db.models.calculation import Calculation
from backend.db.models.material import Material


class CalculationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        user_id: UUID | None,
        source: str,
        calc_version: str,
        input_schema_version: str,
        result_schema_version: str,
        input_data: CalcInputV1,
        planning_requirements: PlanningRequirementsV1,
        calc_result: CalcResultV1,
    ) -> Calculation:

        calc = Calculation(
            id=uuid4(),
            user_id=user_id,
            source=source,
            calc_version=calc_version,
            input_schema_version=input_schema_version,
            result_schema_version=result_schema_version,
            input_data=input_data.dict(),
            planning_requirements=planning_requirements.dict(),
            calc_result=calc_result.dict(),
        )

        self.session.add(calc)
        await self.session.commit()
        await self.session.refresh(calc)

        return calc

    async def get_calculation_by_id(self, calc_id: UUID) -> Calculation | None:
        return await self.session.get(Calculation, calc_id)

    async def get_material_by_section_id(self, section_id) -> Material:
        stmt = select(Material).where(Material.section_id == section_id)
        return await self.session.scalar(stmt)
