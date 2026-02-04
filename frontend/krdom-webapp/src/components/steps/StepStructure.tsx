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
  const wrap: React.CSSProperties = {
    display: "grid",
    gap: 12,
    paddingLeft: 12,
    paddingRight: 12,
  };

  const fieldset: React.CSSProperties = {
    borderRadius: 14,
    padding: 12,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-secondary-bg-color, #f2f2f2)",
  };

  const legend: React.CSSProperties = {
    padding: "0 8px",
    fontSize: 14,
    color: "var(--tg-theme-text-color, #111)",
    opacity: 0.85,
  };

  const row: React.CSSProperties = {
    display: "grid",
    gridTemplateColumns: "170px 1fr",
    alignItems: "center",
    gap: 12,
    paddingTop: 8,
    paddingBottom: 8,
  };

  const label: React.CSSProperties = {
    fontSize: 14,
    color: "var(--tg-theme-text-color, #111)",
    opacity: 0.9,
    lineHeight: 1.2,
  };

  const inputStyle: React.CSSProperties = {
    width: 120,
    justifySelf: "start",
    padding: "10px 12px",
    fontSize: 16,
    borderRadius: 12,
    boxSizing: "border-box",
    background: "var(--tg-theme-bg-color, #fff)",
    color: "var(--tg-theme-text-color, #111)",
    border: "1px solid rgba(0,0,0,0.12)",
    outline: "none",
  };

  const selectStyle: React.CSSProperties = {
    ...inputStyle,
    width: 200,
  };

  const checkboxRow: React.CSSProperties = {
    display: "flex",
    alignItems: "center",
    gap: 10,
    paddingTop: 8,
    paddingBottom: 8,
    color: "var(--tg-theme-text-color, #111)",
    fontSize: 14,
    opacity: 0.9,
  };

  const checkbox: React.CSSProperties = {
    width: 18,
    height: 18,
  };

  return (
    <div style={wrap}>
      {/* Каркас */}
      <fieldset style={fieldset}>
        <legend style={legend}>Каркас</legend>

        <div style={row}>
          <div style={label}>Шаг стоек (м)</div>
          <input
            type="number"
            inputMode="decimal"
            value={input.stud_spacing}
            onChange={(e) =>
              setInput((p) => ({ ...p, stud_spacing: Number(e.target.value) }))
            }
            style={inputStyle}
          />
        </div>

        <div style={row}>
          <div style={label}>Шаг балок перекрытий (м)</div>
          <input
            type="number"
            inputMode="decimal"
            value={input.joist_spacing}
            onChange={(e) =>
              setInput((p) => ({ ...p, joist_spacing: Number(e.target.value) }))
            }
            style={inputStyle}
          />
        </div>

        <div style={row}>
          <div style={label}>Шаг стропил (м)</div>
          <input
            type="number"
            inputMode="decimal"
            value={input.rafter_spacing}
            onChange={(e) =>
              setInput((p) => ({
                ...p,
                rafter_spacing: Number(e.target.value),
              }))
            }
            style={inputStyle}
          />
        </div>
      </fieldset>

      {/* Кровля */}
      <fieldset style={fieldset}>
        <legend style={legend}>Кровля</legend>

        <div style={row}>
          <div style={label}>Угол кровли (°)</div>
          <input
            type="number"
            inputMode="decimal"
            value={input.roof_pitch_deg}
            onChange={(e) =>
              setInput((p) => ({
                ...p,
                roof_pitch_deg: Number(e.target.value),
              }))
            }
            style={inputStyle}
          />
        </div>

        <label style={checkboxRow}>
          <input
            type="checkbox"
            checked={input.is_fronton_short}
            onChange={(e) =>
              setInput((p) => ({ ...p, is_fronton_short: e.target.checked }))
            }
            style={checkbox}
          />
          Фронтон по ширине
        </label>
      </fieldset>

      {/* Сечения */}
      <fieldset style={fieldset}>
        <legend style={legend}>Сечения (section_id)</legend>

        <div style={row}>
          <div style={label}>Стены</div>
          <select
            value={input.wall_section_id}
            onChange={(e) =>
              setInput((p) => ({ ...p, wall_section_id: e.target.value }))
            }
            style={selectStyle}
          >
            {sectionIds.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </select>
        </div>

        <div style={row}>
          <div style={label}>Цокольное перекрытие</div>
          <select
            value={input.ground_overlap_section_id}
            onChange={(e) =>
              setInput((p) => ({
                ...p,
                ground_overlap_section_id: e.target.value,
              }))
            }
            style={selectStyle}
          >
            {sectionIds.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </select>
        </div>

        <div style={row}>
          <div style={label}>Межэтажное перекрытие</div>
          <select
            value={input.interfloor_overlap_section_id}
            onChange={(e) =>
              setInput((p) => ({
                ...p,
                interfloor_overlap_section_id: e.target.value,
              }))
            }
            style={selectStyle}
          >
            {sectionIds.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </select>
        </div>

        <div style={row}>
          <div style={label}>Чердачное перекрытие</div>
          <select
            value={input.attic_overlap_section_id}
            onChange={(e) =>
              setInput((p) => ({
                ...p,
                attic_overlap_section_id: e.target.value,
              }))
            }
            style={selectStyle}
          >
            {sectionIds.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </select>
        </div>

        <div style={row}>
          <div style={label}>Кровля (стропила/конёк)</div>
          <select
            value={input.roof_section_id}
            onChange={(e) =>
              setInput((p) => ({ ...p, roof_section_id: e.target.value }))
            }
            style={selectStyle}
          >
            {sectionIds.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </select>
        </div>

        <div style={row}>
          <div style={label}>Обрешётка</div>
          <select
            value={input.lath_section_id}
            onChange={(e) =>
              setInput((p) => ({ ...p, lath_section_id: e.target.value }))
            }
            style={selectStyle}
          >
            {sectionIds.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </select>
        </div>
      </fieldset>

      {/* Перекрытия */}
      <fieldset style={fieldset}>
        <legend style={legend}>Перекрытия</legend>

        <label style={checkboxRow}>
          <input
            type="checkbox"
            checked={input.has_ground_overlap}
            onChange={(e) =>
              setInput((p) => ({ ...p, has_ground_overlap: e.target.checked }))
            }
            style={checkbox}
          />
          Цокольное перекрытие
        </label>

        <label style={checkboxRow}>
          <input
            type="checkbox"
            checked={input.has_interfloor_overlap}
            onChange={(e) =>
              setInput((p) => ({
                ...p,
                has_interfloor_overlap: e.target.checked,
              }))
            }
            style={checkbox}
          />
          Межэтажное перекрытие
        </label>

        <label style={checkboxRow}>
          <input
            type="checkbox"
            checked={input.has_attic_overlap}
            onChange={(e) =>
              setInput((p) => ({ ...p, has_attic_overlap: e.target.checked }))
            }
            style={checkbox}
          />
          Чердачное перекрытие
        </label>
      </fieldset>
    </div>
  );
}
