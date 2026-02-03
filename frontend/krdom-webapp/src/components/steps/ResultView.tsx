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

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <div style={{ padding: 10, border: "1px solid #ddd", borderRadius: 10 }}>
        <div>
          <b>Итого (м³):</b> {r.summary.volume_total_m3}
        </div>
        <div>
          <b>Без отходов (м³):</b> {r.summary.volume_total_without_waste_m3}
        </div>
        <div>
          <b>Отходы (м³):</b> {r.summary.volume_waste_m3}
        </div>
      </div>

      <div style={{ padding: 10, border: "1px solid #ddd", borderRadius: 10 }}>
        <h3 style={{ marginTop: 0 }}>По сечениям</h3>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>
                section_id
              </th>
              <th
                style={{ textAlign: "right", borderBottom: "1px solid #ccc" }}
              >
                LM
              </th>
              <th
                style={{ textAlign: "right", borderBottom: "1px solid #ccc" }}
              >
                LM+отх
              </th>
              <th
                style={{ textAlign: "right", borderBottom: "1px solid #ccc" }}
              >
                м³
              </th>
            </tr>
          </thead>
          <tbody>
            {r.totals_by_section.map((s) => (
              <tr key={s.section_id}>
                <td>{s.section_id}</td>
                <td style={{ textAlign: "right" }}>{s.lm}</td>
                <td style={{ textAlign: "right" }}>{s.lm_with_waste}</td>
                <td style={{ textAlign: "right" }}>{s.volume_m3}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ padding: 10, border: "1px solid #ddd", borderRadius: 10 }}>
        <h3 style={{ marginTop: 0 }}>По узлам</h3>
        {r.totals_by_group.map((g) => (
          <div key={g.group} style={{ marginBottom: 8 }}>
            <b>{g.group}</b>
            <div style={{ fontSize: 13 }}>
              {g.totals_by_section.map((s) => (
                <div key={s.section_id}>
                  {s.section_id}: {s.volume_m3} м³
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div style={{ padding: 10, border: "1px solid #ddd", borderRadius: 10 }}>
        <h3 style={{ marginTop: 0 }}>По элементам</h3>
        {r.items.map((i) => (
          <div key={i.group} style={{ marginBottom: 8 }}>
            <b>{i.group}</b>
            <div style={{ fontSize: 13 }}>
              <b>{i.element} </b>
              <b>{i.section_id}</b>
            </div>
            <div style={{ fontSize: 13 }}>
              <b>Длина: {i.lm} м. </b>
              <b>Длина с отходами: {i.lm_with_waste} м. </b>
              <b>Объем: {i.volume_m3} м3. </b>
            </div>
          </div>
        ))}
      </div>
      <button onClick={handleExport} disabled={exporting}>
        {exporting ? "Формирование PDF…" : "📄 Скачать PDF"}
      </button>

      <button onClick={onNew}>Новый расчёт</button>
    </div>
  );
}
