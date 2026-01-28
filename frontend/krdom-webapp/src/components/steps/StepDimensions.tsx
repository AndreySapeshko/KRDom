import type { CalcInputV1 } from "../../types/api";

export function StepDimensions({
  input,
  setInput,
}: {
  input: CalcInputV1;
  setInput: (fn: (p: CalcInputV1) => CalcInputV1) => void;
}) {
  return (
    <div style={{ display: "grid", gap: 10 }}>
      <label>
        Длина (м)
        <input type="number" value={input.length} onChange={(e) => setInput((p) => ({ ...p, length: Number(e.target.value) }))} />
      </label>
      <label>
        Ширина (м)
        <input type="number" value={input.width} onChange={(e) => setInput((p) => ({ ...p, width: Number(e.target.value) }))} />
      </label>
      <label>
        Высота стен (м)
        <input type="number" value={input.wall_height} onChange={(e) => setInput((p) => ({ ...p, wall_height: Number(e.target.value) }))} />
      </label>
      <label>
        Этажей
        <input type="number" value={input.total_floors} onChange={(e) => setInput((p) => ({ ...p, total_floors: Number(e.target.value) }))} />
      </label>
    </div>
  );
}
