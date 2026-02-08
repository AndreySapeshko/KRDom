from backend.core.calc.roof_parameters import calc_roof_parameters
from backend.core.models.calc_item import CalcItem
from backend.core.models.summary import CalcSummary

from ..calc.context import CalcContext
from ..calc.floors_ceilings_area import calc_floors_ceilings_area
from ..calc.usable_area_of_boards import calc_usable_area_of_boards
from ..calc.volume_insulation import calc_volume_insulation
from ..calc.walls_area import calc_walls_area
from ..models.totals import SectionTotal
from .rounding import round_volume


def build_summary(
    items: list[CalcItem], waste_factor: float, ctx: CalcContext, totals_by_section: list[SectionTotal]
) -> CalcSummary:
    """Метод собирает итоговые результаты по строению, метод будет расширен, добавлю:
    площадь кровли, площадь свесов, периметр кровли, длинна конька, длинна карниза, длинна торца;
    площадь стен (наружных и внутренних), площадь полов, площадь потолков;
    объем утеплителя, площадь поверхности полезного пиломатериала."""

    volume_without_waste = sum(round_volume(i.volume_m3) for i in items)
    volume_with_waste = volume_without_waste * waste_factor if waste_factor else volume_without_waste
    volume_waste = volume_with_waste - volume_without_waste
    roof_parameters = calc_roof_parameters(ctx)
    walls_area = calc_walls_area(ctx)
    floors_ceilings_area = calc_floors_ceilings_area(ctx)
    total_usable_area_of_board = calc_usable_area_of_boards(ctx, totals_by_section)
    total_volume_insulation = calc_volume_insulation(ctx)
    return CalcSummary(
        waste_factor=waste_factor,
        volume_total_without_waste_m3=round_volume(volume_without_waste),
        volume_total_m3=round_volume(volume_with_waste),
        volume_waste_m3=round_volume(volume_waste),
        total_usable_area_of_board=total_usable_area_of_board,
        total_volume_insulation=total_volume_insulation,
        total_roof_area=roof_parameters.get("total_roof_area"),
        total_overhang_area=roof_parameters.get("total_overhang_area"),
        total_roof_perimeter=roof_parameters.get("total_roof_perimeter"),
        total_length_ridge=roof_parameters.get("total_length_ridge"),
        total_length_gable=roof_parameters.get("total_length_gable"),
        total_length_eave=roof_parameters.get("total_length_eave"),
        total_external_walls_area=walls_area.get("total_external_walls_area"),
        total_internal_walls_area=walls_area.get("total_internal_walls_area"),
        total_ceilings_area=floors_ceilings_area.get("total_ceilings_area"),
        total_floors_area=floors_ceilings_area.get("total_floors_area"),
    )
