"use client";

import { sanitizeOutput } from "@/lib/sanitization";

interface ScriptBoxProps {
  script: string;
  language: string;
  isLoading: boolean;
}

const ScriptBox = ({ script, language, isLoading }: ScriptBoxProps) => {
  if (isLoading) {
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-[var(--text-primary)]">
          📜 Generated Script:
        </h3>
        <div className="command-box animate-pulse-neon">
          <span className="text-[var(--text-muted)]">Generating script...</span>
        </div>
      </div>
    );
  }

  if (!script) {
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-[var(--text-primary)]">
          📜 Generated Script:
        </h3>
        <div className="command-box">
          <span className="text-[var(--neon-red)]">
            No script generated. Try rephrasing your prompt.
          </span>
        </div>
      </div>
    );
  }

  const sanitizedScript = sanitizeOutput(script);

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-[var(--text-primary)]">
        📜 Generated Script ({language}):
      </h3>
      <div className="command-box group relative max-h-96 overflow-y-auto">
        <pre className="text-[var(--text-secondary)] whitespace-pre-wrap break-words">
          <code>{sanitizedScript}</code>
        </pre>
        <button
          onClick={() => navigator.clipboard?.writeText(sanitizedScript)}
          className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity
                     text-[var(--text-muted)] hover:text-[var(--text-primary)] text-sm"
          title="Copy to clipboard"
        >
          📋
        </button>
      </div>
    </div>
  );
};

export default ScriptBox;
