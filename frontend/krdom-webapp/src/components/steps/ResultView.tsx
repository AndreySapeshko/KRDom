import { useState } from "react";
import type { CalcResponseV1 } from "../../types/api";
import { exportPdf } from "../../api/export";

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

  const handleExport = async () => {
    try {
      setExporting(true);
      const blob = await exportPdf(calcId);

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `krdom_${calcId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      console.error(e);
      alert("Ошибка при экспорте PDF");
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
  };

  const row: React.CSSProperties = {
    display: "flex",
    justifyContent: "space-between",
    flexWrap: "wrap",
    gap: 6,
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
    fontWeight: 600,
  };

  const title: React.CSSProperties = {
    fontSize: 16,
    fontWeight: 700,
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
    opacity: 0.9,
  };

  const groupBlock: React.CSSProperties = {
    border: "1px solid rgba(0,0,0,0.08)",
    borderRadius: 12,
    padding: 10,
    background: "var(--tg-theme-bg-color, #fff)",
    marginBottom: 10,
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

  return (
    <div style={wrap}>
      {/* Итог */}
      <div style={card}>
        <div style={title}>Итог</div>
        <div style={row}>
          <span style={label}>Итого (м³)</span>
          <span style={value}>{r.summary.volume_total_m3}</span>
        </div>
        <div style={row}>
          <span style={label}>Без отходов (м³)</span>
          <span style={value}>{r.summary.volume_total_without_waste_m3}</span>
        </div>
        <div style={row}>
          <span style={label}>Отходы (м³)</span>
          <span style={value}>{r.summary.volume_waste_m3}</span>
        </div>
      </div>

      {/* По сечениям */}
      <div style={card}>
        <div style={title}>По сечениям</div>
        {r.totals_by_section.map((s) => (
          <div key={s.section_id} style={row}>
            <span style={sectionChip}>{s.section_id}</span>
            <span style={smallText}>LM: {s.lm}</span>
            <span style={smallText}>LM+отх: {s.lm_with_waste}</span>
            <span style={smallText}>м³: {s.volume_m3}</span>
          </div>
        ))}
      </div>

      {/* По узлам */}
      <div style={card}>
        <div style={title}>По узлам</div>
        {r.totals_by_group.map((g) => (
          <div key={g.group} style={groupBlock}>
            <div style={{ fontSize: 14, fontWeight: 700, marginBottom: 6 }}>
              {g.group}
            </div>
            {g.totals_by_section.map((s) => (
              <div key={s.section_id} style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <span style={sectionChip}>{s.section_id}</span>
                <span style={smallText}>{s.volume_m3} м³</span>
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* По элементам */}
      <div style={card}>
        <div style={title}>По элементам</div>
        {r.items.map((i, idx) => (
          <div key={`${i.group}_${i.element}_${idx}`} style={groupBlock}>
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginBottom: 6 }}>
              <div style={{ fontSize: 14, fontWeight: 700 }}>{i.group}</div>
              <div style={smallText}>
                {i.element} <span style={sectionChip}>{i.section_id}</span>
              </div>
            </div>
            <div style={smallText}><b>Длина:</b> {i.lm} м</div>
            <div style={smallText}><b>Длина с отходами:</b> {i.lm_with_waste} м</div>
            <div style={smallText}><b>Объем:</b> {i.volume_m3} м³</div>
          </div>
        ))}
      </div>

      {/* Кнопки */}
      <button style={buttonPrimary} onClick={handleExport} disabled={exporting}>
        {exporting ? "Формирование PDF…" : "📄 Скачать PDF"}
      </button>

      <button style={buttonSecondary} onClick={onNew}>
        Новый расчёт
      </button>
    </div>
  );
}
