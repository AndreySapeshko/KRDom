export function Stepper({
  step,
  steps,
}: {
  step: number;
  steps: string[];
}) {
  const wrap: React.CSSProperties = {
    display: "flex",
    flexWrap: "wrap",         // переносим пилюли на следующую строку при нехватке места
    gap: 8,
    marginBottom: 12,
  };

  const pillBase: React.CSSProperties = {
    flex: "1 1 120px",        // гибкая ширина: минимум 120px, растягивается при необходимости
    padding: "8px 12px",
    borderRadius: 999,
    border: "1px solid rgba(52, 52, 52, 0.12)",
    fontSize: 13,
    lineHeight: 1,
    userSelect: "none",
    textAlign: "center",
    boxSizing: "border-box",
    whiteSpace: "nowrap",
  };

  const pillActive: React.CSSProperties = {
    background: "var(--tg-theme-button-color, #2481cc)",
    color: "var(--tg-theme-button-text-color, #fff)",
    border: "1px solid rgba(0,0,0,0.0)",
    fontWeight: 700,
  };

  const pillDone: React.CSSProperties = {
    background: "var(--tg-theme-secondary-bg-color, #f2f2f2)",
    color: "var(--tg-theme-text-color, #9c9c9c)",
    opacity: 0.9,
  };

  const pillFuture: React.CSSProperties = {
    background: "var(--tg-theme-bg-color, #fff)",
    color: "var(--tg-theme-hint-color, #4f4f4f)",
    opacity: 0.9,
  };

  return (
    <div style={wrap}>
      {steps.map((title, i) => {
        const style =
          i === step
            ? { ...pillBase, ...pillActive }
            : i < step
              ? { ...pillBase, ...pillDone }
              : { ...pillBase, ...pillFuture };

        return (
          <div key={title} style={style}>
            {i + 1}. {title}
          </div>
        );
      })}
    </div>
  );
}
