import { useState } from "react";
import type { CalcInputV1, OpeningIn, InternalWallIn, OpeningType } from "../../types/api";

export function StepOpenings({
  input,
  setInput,
  addExternal,
  addInternal,
}: {
  input: CalcInputV1;
  setInput: (fn: (p: CalcInputV1) => CalcInputV1) => void;
  addExternal: (o: OpeningIn) => void;
  addInternal: (w: InternalWallIn) => void;
}) {
  const [ext, setExt] = useState<OpeningIn>({ type: "WINDOW", width: 1.2, height: 1.4, quantity: 1 });
  const [wallLen, setWallLen] = useState<number>(5.7);

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
    display: "grid",
    gap: 10,
  };

  const legend: React.CSSProperties = {
    fontWeight: 600,
    fontSize: 14,
    color: "var(--tg-theme-text-color, #111)",
    opacity: 0.85,
  };

  const row: React.CSSProperties = {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 10,
  };

  const inputStyle: React.CSSProperties = {
    width: 100,
    padding: "8px 10px",
    borderRadius: 12,
    fontSize: 14,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-bg-color, #fff)",
    color: "var(--tg-theme-text-color, #111)",
    boxSizing: "border-box",
  };

  const buttonStyle: React.CSSProperties = {
    padding: "10px 14px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-button-color, #2481cc)",
    color: "var(--tg-theme-button-text-color, #fff)",
    fontSize: 14,
    cursor: "pointer",
  };

  const chip: React.CSSProperties = {
    display: "inline-block",
    padding: "2px 6px",
    borderRadius: 999,
    background: "var(--tg-theme-bg-color, #fff)",
    border: "1px solid rgba(0,0,0,0.1)",
    fontSize: 13,
    marginRight: 6,
  };

  return (
    <div style={wrap}>
      {/* Наружные проёмы */}
      <fieldset style={fieldset}>
        <div style={legend}>Наружные проёмы</div>

        <div style={row}>
          <select
            value={ext.type}
            onChange={(e) => setExt((p) => ({ ...p, type: e.target.value as OpeningType }))}
            style={inputStyle}
          >
            <option value="WINDOW">Окно</option>
            <option value="DOOR">Дверь</option>
            <option value="PORTAL">Портал</option>
          </select>

          <input
            type="number"
            value={ext.width}
            onChange={(e) => setExt((p) => ({ ...p, width: Number(e.target.value) }))}
            placeholder="Ширина (м)"
            style={inputStyle}
          />
        </div>

        <div style={row}>
          <input
            type="number"
            value={ext.height}
            onChange={(e) => setExt((p) => ({ ...p, height: Number(e.target.value) }))}
            placeholder="Высота (м)"
            style={inputStyle}
          />
          <input
            type="number"
            value={ext.quantity}
            onChange={(e) => setExt((p) => ({ ...p, quantity: Number(e.target.value) }))}
            placeholder="Кол-во"
            style={inputStyle}
          />
        </div>

        <button style={buttonStyle} onClick={() => addExternal(ext)}>
          + Добавить проём
        </button>

        {input.external_openings.length > 0 && (
          <div>
            {input.external_openings.map((o, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 6, marginTop: 6 }}>
                <span style={chip}>{o.type}</span>
                <span>{o.width}×{o.height} × {o.quantity}</span>
                <button
                  style={{ ...buttonStyle, background: "#ddd", color: "#111", padding: "4px 8px", fontSize: 12 }}
                  onClick={() =>
                    setInput((p) => ({
                      ...p,
                      external_openings: p.external_openings.filter((_, idx) => idx !== i),
                    }))
                  }
                >
                  удалить
                </button>
              </div>
            ))}
          </div>
        )}
      </fieldset>

      {/* Внутренние стены */}
      <fieldset style={fieldset}>
        <div style={legend}>Внутренние стены</div>

        <input
          type="number"
          value={wallLen}
          onChange={(e) => setWallLen(Number(e.target.value))}
          placeholder="Длина стены (м)"
          style={inputStyle}
        />

        <button style={buttonStyle} onClick={() => addInternal({ length: wallLen, openings: [] })}>
          + Добавить стену
        </button>

        {input.internal_walls.length > 0 && (
          <div>
            {input.internal_walls.map((w, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 6, marginTop: 6 }}>
                <span>Стена {w.length} м</span>
                <button
                  style={{ ...buttonStyle, background: "#ddd", color: "#111", padding: "4px 8px", fontSize: 12 }}
                  onClick={() =>
                    setInput((p) => ({
                      ...p,
                      internal_walls: p.internal_walls.filter((_, idx) => idx !== i),
                    }))
                  }
                >
                  удалить
                </button>
              </div>
            ))}
          </div>
        )}
      </fieldset>
    </div>
  );
}
