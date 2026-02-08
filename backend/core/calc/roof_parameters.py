from math import cos, radians

from backend.core.aggregators.rounding import round_lm
from backend.core.calc.context import CalcContext
from backend.core.calc.utils import _get_length_width_roof


def calc_roof_parameters(ctx: CalcContext) -> dict:
    roof_length, roof_width = _get_length_width_roof(ctx)
    eave_overhang = ctx.eave_overhang / cos(radians(ctx.roof_pitch_deg))

    total_roof_area = round_lm(roof_width * roof_length * 2)
    total_overhang_area = round_lm(
        roof_width * 4 * ctx.gable_overhang + (roof_length - ctx.gable_overhang * 2) * eave_overhang * 2
    )
    total_roof_perimeter = round_lm((roof_width * 2 + roof_length) * 2)
    total_length_ridge = round_lm(roof_length)
    total_length_gable = round_lm(roof_width * 4)
    total_length_eave = round_lm(roof_length * 2)

    return {
        "total_roof_area": total_roof_area,
        "total_overhang_area": total_overhang_area,
        "total_roof_perimeter": total_roof_perimeter,
        "total_length_ridge": total_length_ridge,
        "total_length_gable": total_length_gable,
        "total_length_eave": total_length_eave,
    }
