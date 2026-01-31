import type { CalcInputV1 } from "../../types/api";

export function StepStructure({
  input,
  setInput,
  sectionIds,
}: {
  input: CalcInputV1;
  setInput: (fn: (p: CalcInputV1) => CalcInputV1) => void;
  sectionIds: string[];
}) {
  return (
    <div style={{ display: "grid", gap: 10 }}>
      <label>
        Шаг стоек (м)
        <input type="number" value={input.stud_spacing} onChange={(e) => setInput((p) => ({ ...p, stud_spacing: Number(e.target.value) }))} />
      </label>
      <label>
        Шаг балок перекрытий (м)
        <input type="number" value={input.joist_spacing} onChange={(e) => setInput((p) => ({ ...p, joist_spacing: Number(e.target.value) }))} />
      </label>
      <label>
        Шаг стропил (м)
        <input type="number" value={input.rafter_spacing} onChange={(e) => setInput((p) => ({ ...p, rafter_spacing: Number(e.target.value) }))} />
      </label>

      <label>
        Угол кровли (°)
        <input type="number" value={input.roof_pitch_deg} onChange={(e) => setInput((p) => ({ ...p, roof_pitch_deg: Number(e.target.value) }))} />
      </label>

      <fieldset style={{ border: "1px solid #ddd", borderRadius: 10, padding: 10 }}>
        <legend>Сечения (section_id)</legend>

        <label>
          Стены
          <select value={input.wall_section_id} onChange={(e) => setInput((p) => ({ ...p, wall_section_id: e.target.value }))}>
            {sectionIds.map((id) => <option key={id} value={id}>{id}</option>)}
          </select>
        </label>

        <label>
          Цокольное перекрытие
          <select value={input.ground_overlap_section_id} onChange={(e) => setInput((p) => ({ ...p, ground_overlap_section_id: e.target.value }))}>
            {sectionIds.map((id) => <option key={id} value={id}>{id}</option>)}
          </select>
        </label>

        <label>
          Межэтажное перекрытие
          <select value={input.interfloor_overlap_section_id} onChange={(e) => setInput((p) => ({ ...p, interfloor_overlap_section_id: e.target.value }))}>
            {sectionIds.map((id) => <option key={id} value={id}>{id}</option>)}
          </select>
        </label>

        <label>
          Чердачное перекрытие
          <select value={input.attic_overlap_section_id} onChange={(e) => setInput((p) => ({ ...p, attic_overlap_section_id: e.target.value }))}>
            {sectionIds.map((id) => <option key={id} value={id}>{id}</option>)}
          </select>
        </label>

        <label>
          Кровля (стропила/конёк)
          <select value={input.roof_section_id} onChange={(e) => setInput((p) => ({ ...p, roof_section_id: e.target.value }))}>
            {sectionIds.map((id) => <option key={id} value={id}>{id}</option>)}
          </select>
        </label>

        <label>
          Обрешётка
          <select value={input.lath_section_id} onChange={(e) => setInput((p) => ({ ...p, lath_section_id: e.target.value }))}>
            {sectionIds.map((id) => <option key={id} value={id}>{id}</option>)}
          </select>
        </label>
      </fieldset>

      <fieldset style={{ border: "1px solid #ddd", borderRadius: 10, padding: 10 }}>
        <legend>Перекрытия</legend>

        <label>
          <input
            type="checkbox"
            checked={input.has_ground_overlap}
            onChange={(e) => setInput((p) => ({ ...p, has_ground_overlap: e.target.checked }))}
          />
          Цокольное перекрытие
        </label>

        <label>
          <input
            type="checkbox"
            checked={input.has_interfloor_overlap}
            onChange={(e) => setInput((p) => ({ ...p, has_interfloor_overlap: e.target.checked }))}
          />
          Межэтажное перекрытие
        </label>

        <label>
          <input
            type="checkbox"
            checked={input.has_attic_overlap}
            onChange={(e) => setInput((p) => ({ ...p, has_attic_overlap: e.target.checked }))}
          />
          Чердачное перекрытие
        </label>
      </fieldset>
    </div>
  );
}
