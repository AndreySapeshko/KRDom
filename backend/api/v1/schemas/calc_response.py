from pydantic import BaseModel


class CalcResponseOutV1(BaseModel):
    calc_id: str
    calc_result: dict
    planning_requirements: dict
