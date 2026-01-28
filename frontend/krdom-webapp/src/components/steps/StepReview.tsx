import type { CalcInputV1 } from "../../types/api";

export function StepReview({
  input,
  onRun,
  loading,
}: {
  input: CalcInputV1;
  sectionIds: string[];
  onRun: () => void;
  loading: boolean;
}) {
  return (
    <div style={{ display: "grid", gap: 10 }}>
      <div style={{ padding: 10, border: "1px solid #ddd", borderRadius: 10 }}>
        <div><b>Дом:</b> {input.width}×{input.length} м, высота стен {input.wall_height} м</div>
        <div><b>Проёмы наружные:</b> {input.external_openings.length}</div>
        <div><b>Внутренние стены:</b> {input.internal_walls.length}</div>
      </div>

      <button onClick={onRun} disabled={loading}>
        {loading ? "Считаю..." : "Рассчитать"}
      </button>
    </div>
  );
}
