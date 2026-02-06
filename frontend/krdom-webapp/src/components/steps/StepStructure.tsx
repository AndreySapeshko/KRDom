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
    gap: 14,
    width: "100%",
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
    display: "flex",
    flexDirection: "column",
    gap: 4,
    width: "100%",
  };

  const label: React.CSSProperties = {
    fontSize: 14,
    color: "var(--tg-theme-text-color, #111)",
    opacity: 0.9,
  };

  const inputStyle: React.CSSProperties = {
    width: "100%",
    padding: "10px 12px",
    fontSize: 16,
    borderRadius: 12,
    boxSizing: "border-box",
    background: "var(--tg-theme-bg-color, #fff)",
    color: "var(--tg-theme-text-color, #111)",
    border: "1px solid rgba(0,0,0,0.12)",
    outline: "none",
  };

  const selectStyle: React.CSSProperties = { ...inputStyle };

  const checkboxRow: React.CSSProperties = {
    display: "flex",
    alignItems: "center",
    gap: 10,
    paddingTop: 6,
    paddingBottom: 6,
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
          <label style={label}>Шаг стоек (м)</label>
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
          <label style={label}>Шаг балок перекрытий (м)</label>
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
          <label style={label}>Шаг стропил (м)</label>
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
          <label style={label}>Угол кровли (°)</label>
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

        <div style={row}>
          <label style={label}>Размер свеса по фронтону (м)</label>
          <input
            type="number"
            inputMode="decimal"
            value={input.gable_overhang}
            onChange={(e) =>
              setInput((p) => ({ ...p, gable_overhang: Number(e.target.value) }))
            }
            style={inputStyle}
          />
        </div>

        <div style={row}>
          <label style={label}>Размер свеса по скату (м)</label>
          <input
            type="number"
            inputMode="decimal"
            value={input.eave_overhang}
            onChange={(e) =>
              setInput((p) => ({ ...p, eave_overhang: Number(e.target.value) }))
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

        {[
          { label: "Стены", key: "wall_section_id" },
          { label: "Цокольное перекрытие", key: "ground_overlap_section_id" },
          {
            label: "Межэтажное перекрытие",
            key: "interfloor_overlap_section_id",
          },
          { label: "Чердачное перекрытие", key: "attic_overlap_section_id" },
          { label: "Кровля (стропила/конёк)", key: "roof_section_id" },
          { label: "Обрешётка", key: "lath_section_id" },
        ].map((item) => (
          <div key={item.key} style={row}>
            <label style={label}>{item.label}</label>
            <select
              value={input[item.key as keyof CalcInputV1] as string}
              onChange={(e) =>
                setInput((p) => ({ ...p, [item.key]: e.target.value }))
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
        ))}
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
        <div style={row}>
          <label style={label}>Распорок в цокольном перекрытии</label>
          <input
            type="number"
            inputMode="numeric"
            value={input.ground_blocking_rows}
            onChange={(e) =>
              setInput((p) => ({ ...p, ground_blocking_rows: Number(e.target.value) }))
            }
            style={inputStyle}
          />
        </div>

        <div style={row}>
          <label style={label}>Распорок в межэтажном перекрытии</label>
          <input
            type="number"
            inputMode="numeric"
            value={input.interfloor_blocking_rows}
            onChange={(e) =>
              setInput((p) => ({ ...p, interfloor_blocking_rows: Number(e.target.value) }))
            }
            style={inputStyle}
          />
        </div>

        <div style={row}>
          <label style={label}>Распорок в чердачном перекрытии</label>
          <input
            type="number"
            inputMode="numeric"
            value={input.attic_blocking_rows}
            onChange={(e) =>
              setInput((p) => ({
                ...p,
                attic_blocking_rows: Number(e.target.value),
              }))
            }
            style={inputStyle}
          />
        </div>
      </fieldset>
    </div>
  );
}
