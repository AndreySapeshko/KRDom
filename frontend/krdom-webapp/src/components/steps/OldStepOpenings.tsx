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

  return (
    <div style={{ display: "grid", gap: 14 }}>
      <fieldset style={{ border: "1px solid #ddd", borderRadius: 10, padding: 10 }}>
        <legend>Наружные проёмы</legend>

        <div style={{ display: "grid", gap: 8 }}>
          <label>
            Тип
            <select value={ext.type} onChange={(e) => setExt((p) => ({ ...p, type: e.target.value as OpeningType }))}>
              <option value="WINDOW">Окно</option>
              <option value="DOOR">Дверь</option>
              <option value="PORTAL">Портал</option>
            </select>
          </label>
          <label>
            Ширина (м)
            <input type="number" value={ext.width} onChange={(e) => setExt((p) => ({ ...p, width: Number(e.target.value) }))} />
          </label>
          <label>
            Высота (м)
            <input type="number" value={ext.height} onChange={(e) => setExt((p) => ({ ...p, height: Number(e.target.value) }))} />
          </label>
          <label>
            Кол-во
            <input type="number" value={ext.quantity} onChange={(e) => setExt((p) => ({ ...p, quantity: Number(e.target.value) }))} />
          </label>

          <button onClick={() => addExternal(ext)}>+ Добавить проём</button>

          {input.external_openings.length > 0 && (
            <div style={{ fontSize: 13 }}>
              {input.external_openings.map((o, i) => (
                <div key={i}>
                  {o.type} {o.width}×{o.height} × {o.quantity}
                  <button
                    style={{ marginLeft: 8 }}
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
        </div>
      </fieldset>

      <fieldset style={{ border: "1px solid #ddd", borderRadius: 10, padding: 10 }}>
        <legend>Внутренние стены</legend>

        <label>
          Длина стены (м)
          <input type="number" value={wallLen} onChange={(e) => setWallLen(Number(e.target.value))} />
        </label>

        <button onClick={() => addInternal({ length: wallLen, openings: [] })}>+ Добавить стену</button>

        {input.internal_walls.length > 0 && (
          <div style={{ fontSize: 13 }}>
            {input.internal_walls.map((w, i) => (
              <div key={i}>
                Стена {w.length} м
                <button
                  style={{ marginLeft: 8 }}
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
