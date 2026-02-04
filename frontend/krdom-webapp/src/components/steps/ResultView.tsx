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

  /* ───────────────────────── styles ───────────────────────── */

  const wrap: React.CSSProperties = {
    display: "grid",
    gap: 12,
    paddingLeft: 12,
    paddingRight: 12,
  };

  const card: React.CSSProperties = {
    borderRadius: 14,
    padding: 12,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-secondary-bg-color, #f2f2f2)",
  };

  const title: React.CSSProperties = {
    marginTop: 0,
    marginBottom: 10,
    fontSize: 16,
    color: "var(--tg-theme-text-color, #111)",
    opacity: 0.9,
  };

  const row: React.CSSProperties = {
    display: "grid",
    gridTemplateColumns: "190px 1fr",
    alignItems: "center",
    gap: 12,
    paddingTop: 6,
    paddingBottom: 6,
  };

  const label: React.CSSProperties = {
    fontSize: 14,
    color: "var(--tg-theme-text-color, #111)",
    opacity: 0.85,
  };

  const value: React.CSSProperties = {
    fontSize: 15,
    color: "var(--tg-theme-text-color, #111)",
    fontWeight: 600,
    justifySelf: "start",
  };

  const table: React.CSSProperties = {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: 13,
    color: "var(--tg-theme-text-color, #111)",
  };

  const th: React.CSSProperties = {
    textAlign: "left",
    padding: "8px 6px",
    borderBottom: "1px solid rgba(0,0,0,0.12)",
    opacity: 0.85,
    fontWeight: 600,
  };

  const thRight: React.CSSProperties = {
    ...th,
    textAlign: "right",
  };

  const td: React.CSSProperties = {
    padding: "8px 6px",
    borderBottom: "1px solid rgba(0,0,0,0.06)",
    verticalAlign: "top",
  };

  const tdRight: React.CSSProperties = {
    ...td,
    textAlign: "right",
    fontVariantNumeric: "tabular-nums",
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

  const buttonPrimary: React.CSSProperties = {
    justifySelf: "start",
    padding: "12px 14px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-button-color, #2481cc)",
    color: "var(--tg-theme-button-text-color, #fff)",
    fontSize: 15,
    cursor: exporting ? "default" : "pointer",
    opacity: exporting ? 0.7 : 1,
  };

  const buttonSecondary: React.CSSProperties = {
    justifySelf: "start",
    padding: "12px 14px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-bg-color, #fff)",
    color: "var(--tg-theme-text-color, #111)",
    fontSize: 15,
    cursor: "pointer",
    opacity: 0.95,
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

  return (
    <div style={wrap}>
      {/* Summary */}
      <div style={card}>
        <div style={title}>Итог</div>

        <div style={row}>
          <div style={label}>Итого (м³)</div>
          <div style={value}>{r.summary.volume_total_m3}</div>
        </div>

        <div style={row}>
          <div style={label}>Без отходов (м³)</div>
          <div style={value}>{r.summary.volume_total_without_waste_m3}</div>
        </div>

        <div style={row}>
          <div style={label}>Отходы (м³)</div>
          <div style={value}>{r.summary.volume_waste_m3}</div>
        </div>
      </div>

      {/* Totals by section */}
      <div style={card}>
        <div style={title}>По сечениям</div>

        <table style={table}>
          <thead>
            <tr>
              <th style={th}>section_id</th>
              <th style={thRight}>LM</th>
              <th style={thRight}>LM+отх</th>
              <th style={thRight}>м³</th>
            </tr>
          </thead>

          <tbody>
            {r.totals_by_section.map((s) => (
              <tr key={s.section_id}>
                <td style={td}>
                  <span style={sectionChip}>{s.section_id}</span>
                </td>
                <td style={tdRight}>{s.lm}</td>
                <td style={tdRight}>{s.lm_with_waste}</td>
                <td style={tdRight}>{s.volume_m3}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Totals by group */}
      <div style={card}>
        <div style={title}>По узлам</div>

        {r.totals_by_group.map((g) => (
          <div key={g.group} style={groupBlock}>
            <div
              style={{
                fontSize: 14,
                fontWeight: 700,
                color: "var(--tg-theme-text-color, #111)",
                marginBottom: 6,
              }}
            >
              {g.group}
            </div>

            <div style={{ display: "grid", gap: 4 }}>
              {g.totals_by_section.map((s) => (
                <div
                  key={s.section_id}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 10,
                  }}
                >
                  <span style={sectionChip}>{s.section_id}</span>
                  <span style={smallText}>{s.volume_m3} м³</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Items */}
      <div style={card}>
        <div style={title}>По элементам</div>

        <div style={{ display: "grid", gap: 10 }}>
          {r.items.map((i, idx) => (
            <div key={`${i.group}_${i.element}_${idx}`} style={groupBlock}>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  flexWrap: "wrap",
                  marginBottom: 6,
                }}
              >
                <div
                  style={{
                    fontSize: 14,
                    fontWeight: 700,
                    color: "var(--tg-theme-text-color, #111)",
                  }}
                >
                  {i.group}
                </div>

                <div style={smallText}>
                  {i.element} <span style={sectionChip}>{i.section_id}</span>
                </div>
              </div>

              <div style={smallText}>
                <b>Длина:</b> {i.lm} м
              </div>
              <div style={smallText}>
                <b>Длина с отходами:</b> {i.lm_with_waste} м
              </div>
              <div style={smallText}>
                <b>Объем:</b> {i.volume_m3} м³
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <button style={buttonPrimary} onClick={handleExport} disabled={exporting}>
        {exporting ? "Формирование PDF…" : "📄 Скачать PDF"}
      </button>

      <button style={buttonSecondary} onClick={onNew}>
        Новый расчёт
      </button>
    </div>
  );
}
