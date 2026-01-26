from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.v1.schemas import CalcInputV1
from backend.core.aggregators.builder import build_calc_result
from backend.core.aggregators.planning_requirements import build_planning_requirements
from backend.core.calc.calc_core import calculate_items
from backend.core.calc.context_builder import build_context_from_input
from backend.db import Calculation
from backend.repositories.calculation import CalculationRepository


class CalculationService:

    def __init__(self, session: AsyncSession):
        self.repo = CalculationRepository(session)

    async def calculate_and_save(
        self,
        input_data: CalcInputV1,
        user_id: UUID | None,
        source: str,
    ) -> Calculation:

        context = await build_context_from_input(self.repo, input_data)
        items = calculate_items(context)
        calc_result = build_calc_result(items, input_data.waste_factor)
        planning_requirements = build_planning_requirements(input_data)

        return await self.repo.create(
            user_id=user_id,
            source=source,
            calc_version="1.0",
            input_schema_version="1.0",
            result_schema_version="1.0",
            input_data=input_data,
            planning_requirements=planning_requirements,
            calc_result=calc_result,
        )
