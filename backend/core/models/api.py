from pydantic import BaseModel

from .calc_result import CalcResultV1
from .planning import PlanningRequirementsV1


class CalcResponseV1(BaseModel):
    calc_id: str
    calc_result: CalcResultV1
    planning_requirements: PlanningRequirementsV1
