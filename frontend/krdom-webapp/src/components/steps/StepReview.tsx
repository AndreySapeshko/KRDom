import type { CalcInputV1 } from "../../types/api";

function countOpenings(input: CalcInputV1) {
  const external = input.external_openings.reduce(
    (sum, o) => sum + (o.quantity ?? 1),
    0
  );

  const internal = input.internal_walls.reduce((sum, w) => {
    return sum + w.openings.reduce((s, o) => s + (o.quantity ?? 1), 0);
  }, 0);

  return {
    external,
    internal,
    total: external + internal,
  };
}

export function StepReview({
  input,
  onRun,
  onBack,
  loading,
}: {
  input: CalcInputV1;
  sectionIds: string[]; // оставляем как было
  onRun: () => void;
  onBack: () => void;
  loading: boolean;
}) {
  const openings = countOpenings(input);

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
    fontWeight: 700,
  };

  const actions: React.CSSProperties = {
    display: "grid",
    gap: 10,
    marginTop: 12,
  };

  const buttonBase: React.CSSProperties = {
    padding: "12px 0",
    borderRadius: 12,
    fontSize: 15,
    cursor: "pointer",
    width: "100%",
  };

  const buttonPrimary: React.CSSProperties = {
    ...buttonBase,
    background: "var(--tg-theme-button-color, #2481cc)",
    color: "var(--tg-theme-button-text-color, #fff)",
    border: "1px solid rgba(0,0,0,0.12)",
    opacity: loading ? 0.7 : 1,
    cursor: loading ? "default" : "pointer",
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
      <div style={card}>
        <div style={row}>
          <span style={label}>Дом</span>
          <span style={value}>{input.width}×{input.length} м</span>
        </div>

        <div style={row}>
          <span style={label}>Высота стен</span>
          <span style={value}>{input.wall_height} м</span>
        </div>

        <div style={row}>
          <span style={label}>Этажей</span>
          <span style={value}>{input.total_floors}</span>
        </div>

        <div style={row}>
          <span style={label}>Угол кровли</span>
          <span style={value}>{input.roof_pitch_deg}°</span>
        </div>

        <div style={row}>
          <span style={label}>Свес по фронтону</span>
          <span style={value}>{input.gable_overhang} м</span>
        </div>

        <div style={row}>
          <span style={label}>Свес по скату</span>
          <span style={value}>{input.eave_overhang} м</span>
        </div>

        <div style={row}>
          <span style={label}>Наружные проёмы</span>
          <span style={value}>{openings.external}</span>
        </div>

        <div style={row}>
          <span style={label}>Проёмы внутри</span>
          <span style={value}>{openings.internal}</span>
        </div>

        <div style={row}>
          <span style={label}>Всего проёмов</span>
          <span style={value}>{openings.total}</span>
        </div>

        <div style={row}>
          <span style={label}>Внутренние стены</span>
          <span style={value}>{input.internal_walls.length}</span>
        </div>
      </div>

      {/* Кнопки */}
      <div style={actions}>
        <button style={buttonSecondary} onClick={onBack} disabled={loading}>
          Назад
        </button>

        <button style={buttonPrimary} onClick={onRun} disabled={loading}>
          {loading ? "Считаю..." : "Рассчитать"}
        </button>
      </div>
    </div>
  );
}
