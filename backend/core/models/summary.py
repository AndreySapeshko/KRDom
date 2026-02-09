from pydantic import BaseModel


class CalcSummary(BaseModel):
    waste_factor: float
    total_usable_area_of_board: float
    volume_total_without_waste_m3: float
    volume_total_m3: float
    volume_waste_m3: float
    total_volume_insulation: float

    total_roof_area: float
    total_overhang_area: float
    total_roof_perimeter: float
    total_length_ridge: float
    total_length_gable: float
    total_length_eave: float

    total_external_walls_area: float
    total_internal_walls_area: float
    total_ceilings_area: float
    total_floors_area: float
    width_building: float
    length_building: float
    height_building: float
    roof_pitch_deg: float
