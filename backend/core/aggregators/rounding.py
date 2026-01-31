from decimal import ROUND_HALF_UP, Decimal


def round_lm(value: float) -> float:
    return float(Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def round_volume(value: float) -> float:
    return float(Decimal(value).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))
