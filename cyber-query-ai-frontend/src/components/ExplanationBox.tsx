"use client";

interface ExplanationBoxProps {
  explanation: string;
  isLoading: boolean;
}

const ExplanationBox = ({ explanation, isLoading }: ExplanationBoxProps) => {
  if (isLoading) {
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-[var(--text-primary)]">
          📖 Explanation:
        </h3>
        <div className="terminal-border rounded-lg p-4 animate-pulse-neon">
          <div className="text-[var(--text-muted)]">
            Generating explanation...
          </div>
        </div>
      </div>
    );
  }

  if (!explanation) {
    return null;
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-[var(--text-primary)]">
        📖 Explanation:
      </h3>
      <div className="terminal-border rounded-lg p-4 max-h-64 overflow-y-auto">
        <div className="text-[var(--text-secondary)] whitespace-pre-wrap">
          {explanation}
        </div>
      </div>
    </div>
  );
};

export default ExplanationBox;
