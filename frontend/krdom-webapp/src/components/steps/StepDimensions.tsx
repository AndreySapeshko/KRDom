import type { CalcInputV1 } from "../../types/api";

export function StepDimensions({
  input,
  setInput,
}: {
  input: CalcInputV1;
  setInput: (fn: (p: CalcInputV1) => CalcInputV1) => void;
}) {
  const wrap: React.CSSProperties = {
    display: "grid",
    gap: 14,
    width: "100%",
  };

  const subheader: React.CSSProperties = {
    margin: "0 0 12px",
    fontSize: 15,
    opacity: 0.75,
  };

  const row: React.CSSProperties = {
    display: "flex",
    flexDirection: "column",
    gap: 4,
    width: "100%",
  };

  const label: React.CSSProperties = {
    fontSize: 14,
    color: "var(--tg-theme-text-color, #111)",
    opacity: 0.85,
  };

  const inputStyle: React.CSSProperties = {
    width: "100%",
    padding: "10px 12px",
    fontSize: 16,
    borderRadius: 12,
    boxSizing: "border-box",
    background: "var(--tg-theme-secondary-bg-color, #f2f2f2)",
    color: "var(--tg-theme-text-color, #111)",
    border: "1px solid rgba(0,0,0,0.12)",
    outline: "none",
  };

  return (
    <div style={wrap}>
      <div style={subheader}>
        Укажите размеры дома по наружным габаритам
      </div>
      <div style={row}>
        <label style={label}>Длина (м)</label>
        <input
          type="number"
          inputMode="decimal"
          value={input.length}
          onChange={(e) => setInput((p) => ({ ...p, length: Number(e.target.value) }))}
          style={inputStyle}
        />
      </div>

      <div style={row}>
        <label style={label}>Ширина (м)</label>
        <input
          type="number"
          inputMode="decimal"
          value={input.width}
          onChange={(e) => setInput((p) => ({ ...p, width: Number(e.target.value) }))}
          style={inputStyle}
        />
      </div>

      <div style={row}>
        <label style={label}>Высота этажа (м)</label>
        <input
          type="number"
          inputMode="decimal"
          value={input.wall_height}
          onChange={(e) => setInput((p) => ({ ...p, wall_height: Number(e.target.value) }))}
          style={inputStyle}
        />
      </div>

      <div style={row}>
        <label style={label}>Этажей</label>
        <input
          type="number"
          inputMode="numeric"
          value={input.total_floors}
          onChange={(e) => setInput((p) => ({ ...p, total_floors: Number(e.target.value) }))}
          style={inputStyle}
        />
      </div>
    </div>
  );
}
