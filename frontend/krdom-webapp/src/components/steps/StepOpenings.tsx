import { useState } from "react";
import type {
  CalcInputV1,
  OpeningIn,
  InternalWallIn,
  OpeningType,
} from "../../types/api";

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
  /* ───────────────────────── наружные проёмы ───────────────────────── */

  const [ext, setExt] = useState<OpeningIn>({
    type: "WINDOW",
    width: 1.2,
    height: 1.4,
    quantity: 1,
  });

  /* ───────────────────────── внутренние стены ───────────────────────── */

  const [wallLen, setWallLen] = useState<number>(5.7);

  const [intOpening, setIntOpening] = useState<OpeningIn>({
    type: "DOOR",
    width: 0.9,
    height: 2.0,
    quantity: 1,
  });

  /* ───────────────────────── styles ───────────────────────── */

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

  const button: React.CSSProperties = {
    justifySelf: "start",
    padding: "10px 12px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-button-color, #2481cc)",
    color: "var(--tg-theme-button-text-color, #fff)",
    fontSize: 14,
    cursor: "pointer",
  };

  const buttonDanger: React.CSSProperties = {
    padding: "6px 10px",
    borderRadius: 10,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "transparent",
    color: "var(--tg-theme-link-color, #2481cc)",
    fontSize: 13,
    cursor: "pointer",
  };

  const card: React.CSSProperties = {
    border: "1px solid rgba(0,0,0,0.08)",
    borderRadius: 12,
    padding: 10,
    background: "var(--tg-theme-bg-color, #fff)",
  };

  const smallText: React.CSSProperties = {
    fontSize: 13,
    color: "var(--tg-theme-text-color, #111)",
    opacity: 0.9,
  };

  return (
    <div style={wrap}>
      {/* ─────────────── наружные проёмы ─────────────── */}

      <fieldset style={fieldset}>
        <legend style={legend}>Наружные проёмы</legend>

        <div style={row}>
          <div style={label}>Тип</div>
          <select
            value={ext.type}
            onChange={(e) =>
              setExt((p) => ({ ...p, type: e.target.value as OpeningType }))
            }
            style={selectStyle}
          >
            <option value="WINDOW">Окно</option>
            <option value="DOOR">Дверь</option>
            <option value="PORTAL">Портал</option>
          </select>
        </div>

        <div style={row}>
          <div style={label}>Ширина (м)</div>
          <input
            type="number"
            inputMode="decimal"
            value={ext.width}
            onChange={(e) =>
              setExt((p) => ({ ...p, width: Number(e.target.value) }))
            }
            style={inputStyle}
          />
        </div>

        <div style={row}>
          <div style={label}>Высота (м)</div>
          <input
            type="number"
            inputMode="decimal"
            value={ext.height}
            onChange={(e) =>
              setExt((p) => ({ ...p, height: Number(e.target.value) }))
            }
            style={inputStyle}
          />
        </div>

        <div style={row}>
          <div style={label}>Кол-во</div>
          <input
            type="number"
            inputMode="numeric"
            value={ext.quantity}
            onChange={(e) =>
              setExt((p) => ({ ...p, quantity: Number(e.target.value) }))
            }
            style={inputStyle}
          />
        </div>

        <div style={{ marginTop: 8 }}>
          <button style={button} onClick={() => addExternal(ext)}>
            + Добавить проём
          </button>
        </div>

        {input.external_openings.length > 0 && (
          <div style={{ marginTop: 12, display: "grid", gap: 8 }}>
            {input.external_openings.map((o, i) => (
              <div key={i} style={card}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <div style={smallText}>
                    {o.type} {o.width}×{o.height} × {o.quantity}
                  </div>

                  <div style={{ marginLeft: "auto" }}>
                    <button
                      style={buttonDanger}
                      onClick={() =>
                        setInput((p) => ({
                          ...p,
                          external_openings: p.external_openings.filter(
                            (_, idx) => idx !== i
                          ),
                        }))
                      }
                    >
                      удалить
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </fieldset>

      {/* ─────────────── внутренние стены ─────────────── */}

      <fieldset style={fieldset}>
        <legend style={legend}>Внутренние стены</legend>

        <div style={row}>
          <div style={label}>Длина стены (м)</div>
          <input
            type="number"
            inputMode="decimal"
            value={wallLen}
            onChange={(e) => setWallLen(Number(e.target.value))}
            style={inputStyle}
          />
        </div>

        <div style={{ marginTop: 8 }}>
          <button
            style={button}
            onClick={() => addInternal({ length: wallLen, openings: [] })}
          >
            + Добавить стену
          </button>
        </div>

        {input.internal_walls.length > 0 && (
          <div style={{ marginTop: 12, display: "grid", gap: 10 }}>
            {input.internal_walls.map((w, i) => (
              <div key={i} style={card}>
                {/* header стены */}
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <div style={smallText}>Стена {w.length} м</div>

                  <div style={{ marginLeft: "auto" }}>
                    <button
                      style={buttonDanger}
                      onClick={() =>
                        setInput((p) => ({
                          ...p,
                          internal_walls: p.internal_walls.filter(
                            (_, idx) => idx !== i
                          ),
                        }))
                      }
                    >
                      удалить стену
                    </button>
                  </div>
                </div>

                {/* список проёмов стены */}
                {w.openings.length > 0 && (
                  <div style={{ marginTop: 10, display: "grid", gap: 6 }}>
                    {w.openings.map((o, j) => (
                      <div
                        key={j}
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 10,
                          padding: "8px 10px",
                          borderRadius: 10,
                          border: "1px solid rgba(0,0,0,0.08)",
                          background: "var(--tg-theme-secondary-bg-color, #f2f2f2)",
                        }}
                      >
                        <div style={smallText}>
                          {o.type} {o.width}×{o.height} × {o.quantity}
                        </div>

                        <div style={{ marginLeft: "auto" }}>
                          <button
                            style={buttonDanger}
                            onClick={() =>
                              setInput((p) => ({
                                ...p,
                                internal_walls: p.internal_walls.map((iw, idx) =>
                                  idx === i
                                    ? {
                                        ...iw,
                                        openings: iw.openings.filter(
                                          (_, oi) => oi !== j
                                        ),
                                      }
                                    : iw
                                ),
                              }))
                            }
                          >
                            удалить
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* добавление проёма */}
                <div style={{ marginTop: 12 }}>
                  <div
                    style={{
                      fontSize: 13,
                      opacity: 0.8,
                      color: "var(--tg-theme-text-color, #111)",
                      marginBottom: 6,
                    }}
                  >
                    Добавить проём в эту стену
                  </div>

                  <div style={row}>
                    <div style={label}>Тип</div>
                    <select
                      value={intOpening.type}
                      onChange={(e) =>
                        setIntOpening((p) => ({
                          ...p,
                          type: e.target.value as OpeningType,
                        }))
                      }
                      style={selectStyle}
                    >
                      <option value="DOOR">Дверь</option>
                      <option value="PORTAL">Портал</option>
                    </select>
                  </div>

                  <div style={row}>
                    <div style={label}>Ширина (м)</div>
                    <input
                      type="number"
                      inputMode="decimal"
                      value={intOpening.width}
                      onChange={(e) =>
                        setIntOpening((p) => ({
                          ...p,
                          width: Number(e.target.value),
                        }))
                      }
                      style={inputStyle}
                    />
                  </div>

                  <div style={row}>
                    <div style={label}>Высота (м)</div>
                    <input
                      type="number"
                      inputMode="decimal"
                      value={intOpening.height}
                      onChange={(e) =>
                        setIntOpening((p) => ({
                          ...p,
                          height: Number(e.target.value),
                        }))
                      }
                      style={inputStyle}
                    />
                  </div>

                  <div style={row}>
                    <div style={label}>Кол-во</div>
                    <input
                      type="number"
                      inputMode="numeric"
                      value={intOpening.quantity}
                      onChange={(e) =>
                        setIntOpening((p) => ({
                          ...p,
                          quantity: Number(e.target.value),
                        }))
                      }
                      style={inputStyle}
                    />
                  </div>

                  <div style={{ marginTop: 8 }}>
                    <button
                      style={button}
                      onClick={() =>
                        setInput((p) => ({
                          ...p,
                          internal_walls: p.internal_walls.map((iw, idx) =>
                            idx === i
                              ? {
                                  ...iw,
                                  openings: [...iw.openings, intOpening],
                                }
                              : iw
                          ),
                        }))
                      }
                    >
                      + Добавить проём
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </fieldset>
    </div>
  );
}
