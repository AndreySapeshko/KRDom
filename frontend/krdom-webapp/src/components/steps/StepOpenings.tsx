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

  // важно: это состояние одно на все стены (как было у тебя)
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

    // чтобы никогда не появлялась горизонтальная прокрутка
    width: "100%",
    boxSizing: "border-box",
    minWidth: 0,
  };

  const fieldset: React.CSSProperties = {
    borderRadius: 18,
    padding: 12,
    border: "1px solid rgba(255,255,255,0.06)",
    background: "var(--tg-theme-secondary-bg-color, rgba(255,255,255,0.04))",

    width: "100%",
    boxSizing: "border-box",
    minWidth: 0,
  };

  const legend: React.CSSProperties = {
    padding: "0 10px",
    fontSize: 14,
    color: "var(--tg-theme-text-color, #fff)",
    opacity: 0.9,
  };

  const block: React.CSSProperties = {
    display: "grid",
    gap: 10,
    width: "100%",
    minWidth: 0,
  };

  const label: React.CSSProperties = {
    fontSize: 13,
    color: "var(--tg-theme-text-color, #fff)",
    opacity: 0.85,
    lineHeight: 1.2,
  };

  const controlBase: React.CSSProperties = {
    width: "100%",
    boxSizing: "border-box",
    minWidth: 0,

    padding: "12px 14px",
    fontSize: 16,
    borderRadius: 14,
    outline: "none",

    background: "rgba(0,0,0,0.18)",
    color: "var(--tg-theme-text-color, #fff)",
    border: "1px solid rgba(255,255,255,0.06)",
  };

  const selectStyle: React.CSSProperties = {
    ...controlBase,
    appearance: "none",
  };

  const buttonPrimary: React.CSSProperties = {
    width: "100%",
    padding: "12px 14px",
    borderRadius: 14,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-button-color, #2481cc)",
    color: "var(--tg-theme-button-text-color, #fff)",
    fontSize: 15,
    cursor: "pointer",
  };

  const listCard: React.CSSProperties = {
    border: "1px solid rgba(255,255,255,0.06)",
    borderRadius: 16,
    padding: 12,
    background: "rgba(0,0,0,0.12)",

    width: "100%",
    boxSizing: "border-box",
    minWidth: 0,
  };

  const smallText: React.CSSProperties = {
    fontSize: 13,
    color: "var(--tg-theme-text-color, #fff)",
    opacity: 0.9,
    lineHeight: 1.35,
  };

  const buttonDanger: React.CSSProperties = {
    padding: "8px 10px",
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.10)",
    background: "transparent",
    color: "var(--tg-theme-link-color, #5aa7ff)",
    fontSize: 13,
    cursor: "pointer",
    whiteSpace: "nowrap",
  };

  const divider: React.CSSProperties = {
    height: 1,
    background: "rgba(255,255,255,0.06)",
    margin: "10px 0",
  };

  return (
    <div style={wrap}>
      {/* ─────────────── наружные проёмы ─────────────── */}

      <fieldset style={fieldset}>
        <legend style={legend}>Наружные проёмы</legend>

        <div style={block}>
          <div>
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

          <div>
            <div style={label}>Ширина (м)</div>
            <input
              type="number"
              inputMode="decimal"
              value={ext.width}
              onChange={(e) =>
                setExt((p) => ({ ...p, width: Number(e.target.value) }))
              }
              style={controlBase}
            />
          </div>

          <div>
            <div style={label}>Высота (м)</div>
            <input
              type="number"
              inputMode="decimal"
              value={ext.height}
              onChange={(e) =>
                setExt((p) => ({ ...p, height: Number(e.target.value) }))
              }
              style={controlBase}
            />
          </div>

          <div>
            <div style={label}>Количество</div>
            <input
              type="number"
              inputMode="numeric"
              value={ext.quantity}
              onChange={(e) =>
                setExt((p) => ({ ...p, quantity: Number(e.target.value) }))
              }
              style={controlBase}
            />
          </div>

          <button style={buttonPrimary} onClick={() => addExternal(ext)}>
            + Добавить проём
          </button>
        </div>

        {input.external_openings.length > 0 && (
          <>
            <div style={divider} />

            <div style={{ display: "grid", gap: 10 }}>
              {input.external_openings.map((o, i) => (
                <div key={i} style={listCard}>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: 10,
                      minWidth: 0,
                    }}
                  >
                    <div style={{ minWidth: 0 }}>
                      <div style={smallText}>
                        <b>{o.type}</b> {o.width}×{o.height}
                      </div>
                      <div style={smallText}>Количество: {o.quantity}</div>
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
          </>
        )}
      </fieldset>

      {/* ─────────────── внутренние стены ─────────────── */}

      <fieldset style={fieldset}>
        <legend style={legend}>Внутренние стены</legend>

        <div style={block}>
          <div>
            <div style={label}>Длина стены (м)</div>
            <input
              type="number"
              inputMode="decimal"
              value={wallLen}
              onChange={(e) => setWallLen(Number(e.target.value))}
              style={controlBase}
            />
          </div>

          <button
            style={buttonPrimary}
            onClick={() => addInternal({ length: wallLen, openings: [] })}
          >
            + Добавить стену
          </button>
        </div>

        {input.internal_walls.length > 0 && (
          <>
            <div style={divider} />

            <div style={{ display: "grid", gap: 12 }}>
              {input.internal_walls.map((w, i) => (
                <div key={i} style={listCard}>
                  {/* header стены */}
                  <div
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: 10,
                      minWidth: 0,
                    }}
                  >
                    <div style={{ minWidth: 0 }}>
                      <div style={smallText}>
                        <b>Стена</b> {w.length} м
                      </div>
                      <div style={smallText}>
                        Проёмов:{" "}
                        {w.openings.reduce(
                          (sum, o) => sum + (o.quantity ?? 1),
                          0
                        )}
                      </div>
                    </div>

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
                    <div style={{ marginTop: 12, display: "grid", gap: 8 }}>
                      {w.openings.map((o, j) => (
                        <div
                          key={j}
                          style={{
                            borderRadius: 14,
                            padding: 10,
                            border: "1px solid rgba(255,255,255,0.06)",
                            background:
                              "var(--tg-theme-secondary-bg-color, rgba(255,255,255,0.04))",
                          }}
                        >
                          <div
                            style={{
                              display: "flex",
                              alignItems: "flex-start",
                              gap: 10,
                              minWidth: 0,
                            }}
                          >
                            <div style={{ minWidth: 0 }}>
                              <div style={smallText}>
                                <b>{o.type}</b> {o.width}×{o.height}
                              </div>
                              <div style={smallText}>
                                Количество: {o.quantity}
                              </div>
                            </div>

                            <div style={{ marginLeft: "auto" }}>
                              <button
                                style={buttonDanger}
                                onClick={() =>
                                  setInput((p) => ({
                                    ...p,
                                    internal_walls: p.internal_walls.map(
                                      (iw, idx) =>
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
                        </div>
                      ))}
                    </div>
                  )}

                  {/* добавление проёма */}
                  <div style={{ marginTop: 14 }}>
                    <div style={{ ...label, marginBottom: 8, opacity: 0.75 }}>
                      Добавить проём в эту стену
                    </div>

                    <div style={block}>
                      <div>
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

                      <div>
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
                          style={controlBase}
                        />
                      </div>

                      <div>
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
                          style={controlBase}
                        />
                      </div>

                      <div>
                        <div style={label}>Количество</div>
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
                          style={controlBase}
                        />
                      </div>

                      <button
                        style={buttonPrimary}
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
          </>
        )}
      </fieldset>
    </div>
  );
}
