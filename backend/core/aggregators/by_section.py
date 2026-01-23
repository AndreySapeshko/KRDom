from collections import defaultdict

from backend.core.models.calc_item import CalcItem
from backend.core.models.totals import SectionTotal

from .rounding import round_lm, round_volume


def aggregate_by_section(items: list[CalcItem]) -> list[SectionTotal]:
    acc = defaultdict(lambda: {"lm": 0.0, "lm_with_waste": 0.0, "volume": 0.0})

    for item in items:
        a = acc[item.section_id]
        a["lm"] += item.lm
        a["lm_with_waste"] += item.lm_with_waste
        a["volume"] += item.volume_m3

    result: list[SectionTotal] = []
    for section_id, v in acc.items():
        result.append(
            SectionTotal(
                section_id=section_id,
                lm=round_lm(v["lm"]),
                lm_with_waste=round_lm(v["lm_with_waste"]),
                volume_m3=round_volume(v["volume"]),
            )
        )

    return sorted(result, key=lambda x: x.section_id)
