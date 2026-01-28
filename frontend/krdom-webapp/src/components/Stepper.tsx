type Props = {
  step: number;
  steps: string[];
};

export function Stepper({ step, steps }: Props) {
  return (
    <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 12 }}>
      {steps.map((s, i) => (
        <div
          key={s}
          style={{
            padding: "6px 10px",
            borderRadius: 10,
            border: "1px solid #ccc",
            background: i === step ? "#eee" : "transparent",
            fontSize: 14,
          }}
        >
          {i + 1}. {s}
        </div>
      ))}
    </div>
  );
}
