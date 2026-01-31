from pydantic import BaseModel


class CalcSummary(BaseModel):
    waste_factor: float

    volume_total_without_waste_m3: float
    volume_total_m3: float
    volume_waste_m3: float
