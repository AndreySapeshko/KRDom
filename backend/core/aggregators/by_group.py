from collections import defaultdict

from backend.core.models.calc_item import CalcItem
from backend.core.models.totals import GroupTotal, SectionTotal

from .rounding import round_lm, round_volume


def aggregate_by_group(items: list[CalcItem]) -> list[GroupTotal]:
    acc = defaultdict(lambda: defaultdict(lambda: {"lm": 0.0, "lm_with_waste": 0.0, "volume": 0.0}))

    for item in items:
        a = acc[item.group][item.section_id]
        a["lm"] += round_lm(item.lm)
        a["lm_with_waste"] += round_lm(item.lm_with_waste)
        a["volume"] += round_volume(item.volume_m3)

    groups: list[GroupTotal] = []

    for group, sections in acc.items():
        totals = []
        for section_id, v in sections.items():
            totals.append(
                SectionTotal(
                    section_id=section_id,
                    lm=round_lm(v["lm"]),
                    lm_with_waste=round_lm(v["lm_with_waste"]),
                    volume_m3=round_volume(v["volume"]),
                )
            )

        groups.append(GroupTotal(group=group, totals_by_section=sorted(totals, key=lambda x: x.section_id)))

    return sorted(groups, key=lambda g: g.group)
