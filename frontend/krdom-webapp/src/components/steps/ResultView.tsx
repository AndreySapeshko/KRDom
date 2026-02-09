import { useMemo, useState } from "react";
import type { CalcResponseV1, GroupEnum, ElementEnum } from "../../types/api";
import { http } from "../../api/http";
//import { getTg } from "../../tg/telegram";

/* ───────────────────────── translations ───────────────────────── */

const GROUP_LABEL: Record<GroupEnum, string> = {
  EXTERNAL_WALLS: "Наружные стены",
  INTERNAL_WALLS: "Внутренние стены",
  GROUND_OVERLAP: "Цокольное перекрытие",
  INTERFLOOR_OVERLAP: "Межэтажное перекрытие",
  ATTIC_OVERLAP: "Чердачное перекрытие",
  ROOF_STRUCT: "Кровля",
};

const GROUP_ORDER: GroupEnum[] = [
  "EXTERNAL_WALLS",
  "INTERNAL_WALLS",
  "GROUND_OVERLAP",
  "INTERFLOOR_OVERLAP",
  "ATTIC_OVERLAP",
  "ROOF_STRUCT",
];

const ELEMENT_LABEL: Record<ElementEnum, string> = {
  STUDS: "Стойки",
  PLATES_BOTTOM: "Нижняя обвязка стен",
  PLATES_TOP: "Верхняя обвязка стен",
  OPENING_FRAME: "Каркас проёма",
  JOISTS: "Балки",
  RIM: "Наружная обвязка перекрытия",
  BLOCKING: "Распорки перекрытия",
  RAFTERS: "Стропила",
  RIDGE: "Коньковая доска",
  TIES: "Связи",
  LATH: "Обрешётка",
  COUNTER_LATH: "Контр обрешётка",
};

function groupLabel(group: string) {
  return (GROUP_LABEL as Record<string, string>)[group] ?? group;
}

function elementLabel(element: string) {
  return (ELEMENT_LABEL as Record<string, string>)[element] ?? element;
}

function groupSort(a: { group: string }, b: { group: string }) {
  const ai = GROUP_ORDER.indexOf(a.group as GroupEnum);
  const bi = GROUP_ORDER.indexOf(b.group as GroupEnum);

  const ax = ai === -1 ? 999 : ai;
  const bx = bi === -1 ? 999 : bi;

  return ax - bx;
}

/* ───────────────────────── section_id → label ───────────────────────── */

/**
 * BOARD_50x200x6 -> Доска 50×200×6 м
 * BAR_100x100x6 -> Брус 100×100×6 м
 * (если формат не совпал — вернём как есть)
 */
function sectionLabel(sectionId: string) {
  const m = sectionId.match(/^([A-Z]+)_(\d+)x(\d+)x([\d.]+)$/);
  if (!m) return sectionId;

  const kind = m[1];
  const a = m[2];
  const b = m[3];
  const len = m[4];

  const kindRu =
    kind === "BOARD"
      ? "Доска"
      : kind === "BAR"
        ? "Брус"
        : kind === "BEAM"
          ? "Балка"
          : kind;

  // len может быть "6" или "6.0"
  const lenFixed = Number(len).toString().replace(".", ",");

  return `${kindRu} ${a}×${b}×${lenFixed} м`;
}

/* ───────────────────────── helpers ───────────────────────── */

function fmt(n: number) {
  // чтобы 1.000000 не выводилось
  const s = n.toFixed(6);
  return s.replace(/\.?0+$/, "");
}

/* ───────────────────────── component ───────────────────────── */

export function ResultView({
  result,
  onNew,
}: {
  result: CalcResponseV1;
  onNew: () => void;
}) {
  const r = result.calc_result;
  const calcId = result.calc_id;

  const [exporting, setExporting] = useState(false);

  // По узлам: отсортируем группы
  const totalsByGroupSorted = useMemo(() => {
    return [...r.totals_by_group].sort(groupSort);
  }, [r.totals_by_group]);

  // По элементам: сгруппируем
  const itemsByGroup = useMemo(() => {
    const map = new Map<string, typeof r.items>();

    for (const it of r.items) {
      const list = map.get(it.group) ?? [];
      list.push(it);
      map.set(it.group, list);
    }

    const entries = [...map.entries()].map(([group, items]) => ({
      group,
      items: items.sort((a, b) => {
        const ea = elementLabel(a.element);
        const eb = elementLabel(b.element);
        if (ea !== eb) return ea.localeCompare(eb, "ru");
        return sectionLabel(a.section_id).localeCompare(
          sectionLabel(b.section_id),
          "ru",
        );
      }),
    }));

    return entries.sort(groupSort);
  }, [r]);

  // UI state: весь блок "По элементам" свернут по умолчанию
  const [itemsCollapsed, setItemsCollapsed] = useState(true);

  // UI state: какие группы раскрыты
  const [openGroups, setOpenGroups] = useState<Record<string, boolean>>({});

  const toggleGroup = (group: string) => {
    setOpenGroups((p) => ({ ...p, [group]: !p[group] }));
  };

  // const handleExport = async () => {
  //   try {
  //     setExporting(true);

  //     const res = await http.get(`/calc/${calcId}/export/pdf-link`);

  //     const url = res.data.url;

  //     const tg = getTg();
  //     tg?.openLink(url);
  //   } catch (e) {
  //     console.error(e);
  //     alert("Ошибка при открытии PDF");
  //   } finally {
  //     setExporting(false);
  //   }
  // };

  const handleSendToChat = async () => {
    try {
      setExporting(true);

      await http.post(`/calc/${calcId}/export/send-to-chat`);
      alert("Отчёт отправлен в чат!");
    } catch (e) {
      console.error(e);
      alert("Ошибка при открытии PDF");
    } finally {
      setExporting(false);
    }
  };

  /* ──────────────── styles ──────────────── */

  const wrap: React.CSSProperties = {
    display: "grid",
    gap: 14,
    width: "100%",
  };

  const card: React.CSSProperties = {
    borderRadius: 14,
    padding: 14,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-secondary-bg-color, #f2f2f2)",
    display: "grid",
    gap: 10,
    minWidth: 0,
  };

  const row: React.CSSProperties = {
    display: "flex",
    justifyContent: "space-between",
    flexWrap: "wrap",
    gap: 6,
    minWidth: 0,
  };

  const label: React.CSSProperties = {
    fontSize: 14,
    color: "var(--tg-theme-text-color, #111)",
    opacity: 0.85,
    minWidth: 120,
  };

  const value: React.CSSProperties = {
    fontSize: 15,
    color: "var(--tg-theme-text-color, #111)",
    fontWeight: 700,
  };

  const title: React.CSSProperties = {
    fontSize: 16,
    fontWeight: 800,
    color: "var(--tg-theme-text-color, #111)",
    marginBottom: 6,
  };

  const sectionChip: React.CSSProperties = {
    display: "inline-block",
    padding: "4px 8px",
    borderRadius: 999,
    fontSize: 12,
    border: "1px solid rgba(0,0,0,0.10)",
    background: "var(--tg-theme-bg-color, #fff)",
    opacity: 0.95,
    maxWidth: "100%",
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  };

  const groupBlock: React.CSSProperties = {
    border: "1px solid rgba(0,0,0,0.08)",
    borderRadius: 12,
    padding: 10,
    background: "var(--tg-theme-bg-color, #fff)",
    marginBottom: 10,
    minWidth: 0,
  };

  const smallText: React.CSSProperties = {
    fontSize: 13,
    color: "var(--tg-theme-text-color, #111)",
    opacity: 0.9,
    lineHeight: 1.35,
  };

  const buttonBase: React.CSSProperties = {
    padding: "12px 0",
    borderRadius: 12,
    fontSize: 15,
    width: "100%",
    cursor: "pointer",
  };

  const buttonPrimary: React.CSSProperties = {
    ...buttonBase,
    background: "var(--tg-theme-button-color, #2481cc)",
    color: "var(--tg-theme-button-text-color, #fff)",
    border: "1px solid rgba(0,0,0,0.12)",
    opacity: exporting ? 0.7 : 1,
    cursor: exporting ? "default" : "pointer",
  };

  const buttonSecondary: React.CSSProperties = {
    ...buttonBase,
    background: "var(--tg-theme-bg-color, #fff)",
    color: "var(--tg-theme-text-color, #111)",
    border: "1px solid rgba(0,0,0,0.12)",
    opacity: 0.95,
  };

  const collapseButton: React.CSSProperties = {
    width: "100%",
    textAlign: "left",
    padding: "10px 12px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-bg-color, #fff)",
    color: "var(--tg-theme-text-color, #111)",
    fontSize: 14,
    fontWeight: 800,
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 10,
  };

  const groupToggle: React.CSSProperties = {
    width: "100%",
    textAlign: "left",
    padding: "10px 12px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.10)",
    background: "var(--tg-theme-secondary-bg-color, #f2f2f2)",
    color: "var(--tg-theme-text-color, #111)",
    fontSize: 14,
    fontWeight: 800,
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 10,
  };

  return (
    <div style={wrap}>
      {/* Итог */}
      <div style={card}>
        <div style={title}>Итог</div>

        <div  style={groupBlock}>
          <div style={{ fontSize: 15, fontWeight: 800, marginBottom: 8 }}>
            Параметры дома
          </div>

          <div style={row}>
            <span style={label}>Размер дома (ДхШ, м)</span>
            <span style={value}>
              {fmt(r.summary.length_building)} х {fmt(r.summary.width_building)}
            </span>
          </div>

          <div style={row}>
            <span style={label}>Высота дома в коньке (м)</span>
            <span style={value}>{fmt(r.summary.height_building)}</span>
          </div>

          <div style={row}>
            <span style={label}>Угол кровли </span>
            <span style={value}>{fmt(r.summary.height_building)}°</span>
          </div>

          <div style={row}>
            <span style={label}>Площадь наружных стен (м²)</span>
            <span style={value}>{fmt(r.summary.total_external_walls_area)}</span>
          </div>

          <div style={row}>
            <span style={label}>Площадь внутренних стен (м²)</span>
            <span style={value}>
              {fmt(r.summary.total_internal_walls_area)}
            </span>
          </div>

          <div style={row}>
            <span style={label}>Площадь потолков (м²)</span>
            <span style={value}>{fmt(r.summary.total_ceilings_area)}</span>
          </div>

          <div style={row}>
            <span style={label}>Площадь полов (м²)</span>
            <span style={value}>{fmt(r.summary.total_floors_area)}</span>
          </div>

          <div style={row}>
            <span style={label}>Площадь поверхности пиломатериала (м²)</span>
            <span style={value}>
              {fmt(r.summary.total_usable_area_of_board)}
            </span>
          </div>
        </div>

        <div  style={groupBlock}>
          <div style={{ fontSize: 15, fontWeight: 800, marginBottom: 8 }}>
            Кровля
          </div>

          <div style={row}>
            <span style={label}>Площадь кровли (м²)</span>
            <span style={value}>{fmt(r.summary.total_roof_area)}</span>
          </div>

          <div style={row}>
            <span style={label}>Площадь свесов (м²)</span>
            <span style={value}>
              {fmt(r.summary.total_overhang_area)}
            </span>
          </div>

          <div style={row}>
            <span style={label}>Периметр кровли (м)</span>
            <span style={value}>{fmt(r.summary.total_roof_perimeter)}</span>
          </div>

          <div style={row}>
            <span style={label}>Длина конька (м)</span>
            <span style={value}>{fmt(r.summary.total_length_ridge)}</span>
          </div>

          <div style={row}>
            <span style={label}>Длина торцов (м)</span>
            <span style={value}>{fmt(r.summary.total_length_gable)}</span>
          </div>

          <div style={row}>
            <span style={label}>Длина карнизов (м)</span>
            <span style={value}>{fmt(r.summary.total_length_eave)}</span>
          </div>
        </div>
        
        <div  style={groupBlock}>
          <div style={{ fontSize: 15, fontWeight: 800, marginBottom: 8 }}>
            Материалы
          </div>

          <div style={row}>
            <span style={label}>Итого пиломатериала (м³)</span>
            <span style={value}>{fmt(r.summary.volume_total_m3)}</span>
          </div>

          <div style={row}>
            <span style={label}>Пиломатериал без отходов (м³)</span>
            <span style={value}>
              {fmt(r.summary.volume_total_without_waste_m3)}
            </span>
          </div>

          <div style={row}>
            <span style={label}>Отходы (м³)</span>
            <span style={value}>{fmt(r.summary.volume_waste_m3)}</span>
          </div>

          <div style={row}>
            <span style={label}>Утеплитель (м³)</span>
            <span style={value}>{fmt(r.summary.total_volume_insulation)}</span>
          </div>
        </div>
      </div>

      {/* По сечениям */}
      <div style={card}>
        <div style={title}>По сечениям</div>

        {r.totals_by_section.map((s) => (
          <div
            key={s.section_id}
            style={{
              border: "1px solid rgba(0,0,0,0.08)",
              background: "var(--tg-theme-bg-color, #fff)",
              borderRadius: 12,
              padding: 10,
              display: "grid",
              gap: 6,
              minWidth: 0,
            }}
          >
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <span style={sectionChip}>{sectionLabel(s.section_id)}</span>
              <span style={{ ...smallText, opacity: 0.75 }}>
                {s.section_id}
              </span>
            </div>

            <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              <span style={smallText}>LM: {fmt(s.lm)}</span>
              <span style={smallText}>LM+отх: {fmt(s.lm_with_waste)}</span>
              <span style={smallText}>м³: {fmt(s.volume_m3)}</span>
            </div>
          </div>
        ))}
      </div>

      {/* По узлам */}
      <div style={card}>
        <div style={title}>По узлам</div>

        {totalsByGroupSorted.map((g) => (
          <div key={g.group} style={groupBlock}>
            <div style={{ fontSize: 14, fontWeight: 800, marginBottom: 8 }}>
              {groupLabel(g.group)}
            </div>

            <div style={{ display: "grid", gap: 8 }}>
              {g.totals_by_section.map((s) => (
                <div
                  key={s.section_id}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    gap: 10,
                    alignItems: "center",
                    padding: "8px 10px",
                    borderRadius: 12,
                    border: "1px solid rgba(0,0,0,0.08)",
                    background: "var(--tg-theme-secondary-bg-color, #f2f2f2)",
                    minWidth: 0,
                  }}
                >
                  <div style={{ minWidth: 0 }}>
                    <div style={smallText}>{sectionLabel(s.section_id)}</div>
                    <div style={{ ...smallText, opacity: 0.65 }}>
                      {s.section_id}
                    </div>
                  </div>

                  <div style={{ fontWeight: 800, fontSize: 13 }}>
                    {fmt(s.volume_m3)} м³
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* По элементам (сворачиваемый блок) */}
      <div style={card}>
        <button
          style={collapseButton}
          onClick={() => setItemsCollapsed((p) => !p)}
        >
          <span>По элементам</span>
          <span style={{ opacity: 0.7 }}>
            {itemsCollapsed ? "Развернуть ▾" : "Свернуть ▴"}
          </span>
        </button>

        {!itemsCollapsed && (
          <div style={{ display: "grid", gap: 10 }}>
            {itemsByGroup.map((g) => {
              const opened = !!openGroups[g.group];

              return (
                <div key={g.group} style={groupBlock}>
                  <button
                    style={groupToggle}
                    onClick={() => toggleGroup(g.group)}
                  >
                    <span>{groupLabel(g.group)}</span>
                    <span style={{ opacity: 0.7 }}>{opened ? "▴" : "▾"}</span>
                  </button>

                  {opened && (
                    <div style={{ marginTop: 10, display: "grid", gap: 10 }}>
                      {g.items.map((i, idx) => (
                        <div
                          key={`${i.element}_${i.section_id}_${idx}`}
                          style={{
                            borderRadius: 12,
                            border: "1px solid rgba(0,0,0,0.08)",
                            background: "var(--tg-theme-bg-color, #fff)",
                            padding: 10,
                            display: "grid",
                            gap: 6,
                            minWidth: 0,
                          }}
                        >
                          <div style={{ display: "grid", gap: 4 }}>
                            <div style={{ fontSize: 14, fontWeight: 800 }}>
                              {elementLabel(i.element)}
                            </div>

                            <div
                              style={{
                                display: "flex",
                                gap: 8,
                                flexWrap: "wrap",
                              }}
                            >
                              <span style={sectionChip}>
                                {sectionLabel(i.section_id)}
                              </span>
                              <span style={{ ...smallText, opacity: 0.65 }}>
                                {i.section_id}
                              </span>
                            </div>
                          </div>

                          <div
                            style={{
                              display: "flex",
                              gap: 10,
                              flexWrap: "wrap",
                            }}
                          >
                            <span style={smallText}>
                              <b>Длина:</b> {fmt(i.lm)} м
                            </span>
                            <span style={smallText}>
                              <b>С отходами:</b> {fmt(i.lm_with_waste)} м
                            </span>
                            <span style={smallText}>
                              <b>Объём:</b> {fmt(i.volume_m3)} м³
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Кнопки */}
      <button
        style={buttonPrimary}
        onClick={handleSendToChat}
        disabled={exporting}
      >
        {exporting ? "Формирование PDF…" : "📄 Получить PDF"}
      </button>

      <button style={buttonSecondary} onClick={onNew}>
        Новый расчёт
      </button>
    </div>
  );
}
