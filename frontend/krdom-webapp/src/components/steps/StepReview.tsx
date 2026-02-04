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
  sectionIds: string[]; // (не используется, но оставляем как было)
  onRun: () => void;
  onBack: () => void;
  loading: boolean;
}) {
  const openings = countOpenings(input);

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
    fontWeight: 700,
    justifySelf: "start",
  };

  const actions: React.CSSProperties = {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 10,
    marginTop: 2,
  };

  const buttonPrimary: React.CSSProperties = {
    padding: "12px 14px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-button-color, #2481cc)",
    color: "var(--tg-theme-button-text-color, #fff)",
    fontSize: 15,
    cursor: "pointer",
  };

  const buttonSecondary: React.CSSProperties = {
    padding: "12px 14px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-bg-color, #fff)",
    color: "var(--tg-theme-text-color, #111)",
    fontSize: 15,
    cursor: "pointer",
    opacity: 0.95,
  };

  const buttonDisabled: React.CSSProperties = {
    opacity: 0.6,
    cursor: "default",
  };

  return (
    <div style={wrap}>
      <div style={card}>
        <div style={row}>
          <div style={label}>Дом</div>
          <div style={value}>
            {input.width}×{input.length} м
          </div>
        </div>

        <div style={row}>
          <div style={label}>Высота стен</div>
          <div style={value}>{input.wall_height} м</div>
        </div>

        <div style={row}>
          <div style={label}>Этажей</div>
          <div style={value}>{input.total_floors}</div>
        </div>

        <div style={{ height: 8 }} />

        <div style={row}>
          <div style={label}>Наружные проёмы</div>
          <div style={value}>{openings.external}</div>
        </div>

        <div style={row}>
          <div style={label}>Проёмы внутри</div>
          <div style={value}>{openings.internal}</div>
        </div>

        <div style={row}>
          <div style={label}>Всего проёмов</div>
          <div style={value}>{openings.total}</div>
        </div>

        <div style={row}>
          <div style={label}>Внутренние стены</div>
          <div style={value}>{input.internal_walls.length}</div>
        </div>
      </div>

      {/* кнопки внизу */}
      <div style={actions}>
        <button style={buttonSecondary} onClick={onBack} disabled={loading}>
          Назад
        </button>

        <button
          style={{
            ...buttonPrimary,
            ...(loading ? buttonDisabled : null),
          }}
          onClick={onRun}
          disabled={loading}
        >
          {loading ? "Считаю..." : "Рассчитать"}
        </button>
      </div>
    </div>
  );
}
