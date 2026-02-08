import { useEffect, useMemo, useState } from "react";
import { Stepper } from "../components/Stepper";
import { fetchMaterials } from "../api/materials";
import { calculate } from "../api/calc";
import type {
  CalcInputV1,
  CalcResponseV1,
  Material,
  OpeningIn,
  InternalWallIn,
} from "../types/api";
import { getTg } from "../tg/telegram";
import { ResultView } from "../components/steps/ResultView";
import { StepDimensions } from "../components/steps/StepDimensions";
import { StepStructure } from "../components/steps/StepStructure";
import { StepOpenings } from "../components/steps/StepOpenings";
import { StepReview } from "../components/steps/StepReview";
import axios from "axios";

const steps = [
  "Габариты",
  "Конструктив",
  "Проёмы/перегородки",
  "Проверка",
  "Результат",
];

function defaultInput(): CalcInputV1 {
  return {
    length: 8,
    width: 6,
    wall_height: 2.7,
    total_floors: 1,
    is_fronton_short: true,
    stud_spacing: 0.63,
    joist_spacing: 0.63,
    rafter_spacing: 0.63,
    wall_section_id: "BOARD_50x150x6",
    ground_overlap_section_id: "BOARD_50x200x6",
    interfloor_overlap_section_id: "BOARD_50x200x6",
    attic_overlap_section_id: "BOARD_50x150x6",
    roof_section_id: "BOARD_50x200x6",
    lath_section_id: "BOARD_25x100x6",
    waste_factor: 1.1,
    roof_pitch_deg: 35,
    eave_overhang: 0.6,
    gable_overhang: 0.6,
    lath_step: 0.35,
    ties_enabled: false,
    has_ground_overlap: true,
    has_interfloor_overlap: false,
    has_attic_overlap: true,
    ground_blocking_rows: 1,
    interfloor_blocking_rows: 1,
    attic_blocking_rows: 1,
    external_openings: [],
    internal_walls: [],
  };
}

export function CalculatorPage() {
  const [step, setStep] = useState(0);
  const [materials, setMaterials] = useState<Material[]>([]);
  const [input, setInput] = useState<CalcInputV1>(defaultInput());
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CalcResponseV1 | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const tg = getTg();
    if (tg) {
      tg.ready();
      tg.expand();
    }
  }, []);

  useEffect(() => {
    (async () => {
      try {
        const list = await fetchMaterials();
        setMaterials(list);
      } catch (e: unknown) {
        setError(
          e instanceof Error ? e.message : "Не удалось загрузить материалы",
        );
      }
    })();
  }, []);

  const sectionIds = useMemo(
    () => materials.map((m) => m.section_id).sort(),
    [materials],
  );

  const canNext = () => {
    if (step === 0)
      return input.length > 0 && input.width > 0 && input.wall_height > 0;
    if (step === 1)
      return (
        input.stud_spacing > 0 &&
        input.joist_spacing > 0 &&
        input.rafter_spacing > 0
      );
    return true;
  };

  async function runCalc() {
    setError(null);
    setLoading(true);
    try {
      const res = await calculate(input);
      setResult(res);
      setStep(4);
    } catch (e: unknown) {
      if (axios.isAxiosError(e)) {
        const msg = e.response?.data?.detail ?? e.message ?? "Ошибка расчёта";
        setError(typeof msg === "string" ? msg : JSON.stringify(msg));
      } else if (e instanceof Error) setError(e.message);
      else setError("Ошибка расчёта");
    } finally {
      setLoading(false);
    }
  }

  const goNext = () => canNext() && setStep((s) => Math.min(s + 1, 4));
  const goBack = () => setStep((s) => Math.max(s - 1, 0));

  /* ──────────────── стили ──────────────── */
  const page: React.CSSProperties = {
    padding: 14,
    width: "100%",
    color: "var(--tg-theme-text-color, #111)",
    background: "var(--tg-theme-bg-color, #222)", // общий фон листа
    minHeight: "100vh",
    boxSizing: "border-box",
  };

  const header: React.CSSProperties = {
    margin: "6px 0 10px",
    fontSize: 20,
    fontWeight: 800,
  };
  const subheader: React.CSSProperties = {
    margin: "0 0 12px",
    fontSize: 13,
    opacity: 0.75,
  };

  const errorCard: React.CSSProperties = {
    padding: 12,
    borderRadius: 14,
    border: "1px solid rgba(255,0,0,0.25)",
    background: "rgba(255,0,0,0.06)",
    marginBottom: 12,
    fontSize: 14,
    lineHeight: 1.35,
  };

  const bottomNav: React.CSSProperties = {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 10,
    marginTop: 14,
    width: "100%",
  };

  const buttonPrimary: React.CSSProperties = {
    padding: "12px 14px",
    borderRadius: 12,
    border: "1px solid rgba(0,0,0,0.12)",
    background: "var(--tg-theme-button-color, #2481cc)",
    color: "var(--tg-theme-button-text-color, #fff)",
    fontSize: 15,
    cursor: "pointer",
    width: "100%",
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
    width: "100%",
  };

  const buttonDisabled: React.CSSProperties = {
    opacity: 0.55,
    cursor: "default",
  };

  return (
    <div style={page}>
      <div style={header}>KR.Dom — Калькулятор пиломатериала</div>
      <div style={subheader}>
        Заполни параметры дома — и получишь объём пиломатериала по сечениям и
        узлам.
      </div>

      <Stepper step={step} steps={steps} />

      {error && (
        <div style={errorCard}>
          <b>Ошибка:</b> {error}
        </div>
      )}

      {/* Шаги */}
      {step === 0 && <StepDimensions input={input} setInput={setInput} />}
      {step === 1 && (
        <StepStructure
          input={input}
          setInput={setInput}
          sectionIds={sectionIds}
        />
      )}
      {step === 2 && (
        <StepOpenings
          input={input}
          setInput={setInput}
          addExternal={(o: OpeningIn) =>
            setInput((p) => ({
              ...p,
              external_openings: [...p.external_openings, o],
            }))
          }
          addInternal={(w: InternalWallIn) =>
            setInput((p) => ({
              ...p,
              internal_walls: [...p.internal_walls, w],
            }))
          }
        />
      )}
      {step === 3 && (
        <StepReview
          input={input}
          sectionIds={sectionIds}
          onRun={runCalc}
          onBack={goBack}
          loading={loading}
        />
      )}
      {step === 4 && result && (
        <ResultView
          result={result}
          onNew={() => {
            setResult(null);
            setStep(0);
          }}
        />
      )}

      {/* Нижняя навигация */}
      {step < 3 && (
        <div style={bottomNav}>
          <button
            style={{
              ...buttonSecondary,
              ...(step === 0 ? buttonDisabled : {}),
            }}
            onClick={goBack}
            disabled={step === 0}
          >
            Назад
          </button>
          <button
            style={{ ...buttonPrimary, ...(!canNext() ? buttonDisabled : {}) }}
            onClick={goNext}
            disabled={!canNext()}
          >
            Далее
          </button>
        </div>
      )}
    </div>
  );
}
