from pydantic import BaseModel


class PlanningRequirementsV1(BaseModel):
    version: str = "1.0"
    building: dict
    structural_params: dict
    planning_requirements: dict
    assumptions: list[str]
