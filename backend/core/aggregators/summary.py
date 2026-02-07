from backend.core.models.calc_item import CalcItem
from backend.core.models.summary import CalcSummary

from .rounding import round_volume


def build_summary(items: list[CalcItem], waste_factor: float) -> CalcSummary:
    """Метод собирает итоговые результаты по строению, метод будет расширен, добавлю:
    площадь кровли, площадь свесов, периметр кровли, длинна конька, длинна карниза, длинна торца;
    площадь стен (наружных и внутренних), площадь полов, площадь потолков;
    объем утеплителя, площадь поверхности полезного пиломатериала."""

    volume_without_waste = sum(round_volume(i.volume_m3) for i in items)
    volume_with_waste = volume_without_waste * waste_factor if waste_factor else volume_without_waste
    volume_waste = volume_with_waste - volume_without_waste

    return CalcSummary(
        waste_factor=waste_factor,
        volume_total_without_waste_m3=round_volume(volume_without_waste),
        volume_total_m3=round_volume(volume_with_waste),
        volume_waste_m3=round_volume(volume_waste),
    )
