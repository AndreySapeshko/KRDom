from uuid import UUID

from pydantic import BaseModel


class CalcResponseOutV1(BaseModel):
    calc_version: str
    calc_id: UUID
    calc_result: dict
    planning_requirements: dict
