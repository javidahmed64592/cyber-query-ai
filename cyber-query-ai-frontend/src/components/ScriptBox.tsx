"use client";

import { useState } from "react";

import { sanitizeOutput } from "@/lib/sanitization";

interface ScriptBoxProps {
  script: string;
  language: string;
  isLoading: boolean;
}

const ScriptBox = ({ script, language, isLoading }: ScriptBoxProps) => {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard?.writeText(sanitizeOutput(script));
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch {
      // Failed to copy to clipboard
    }
  };

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
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-[var(--text-primary)]">
          📜 Generated Script ({language}):
        </h3>
        <button
          onClick={handleCopy}
          className="px-3 py-2 bg-[var(--surface-elevated)] hover:bg-[var(--surface-hover)]
                     border border-[var(--border-color)] rounded text-sm
                     text-[var(--text-muted)] hover:text-[var(--text-primary)]
                     transition-all duration-200 flex items-center gap-2"
          title={isCopied ? "Copied!" : "Copy to clipboard"}
        >
          {isCopied ? "✓" : "📋"}
          <span>{isCopied ? "Copied" : "Copy Script"}</span>
        </button>
      </div>
      <div className="command-box max-h-96 overflow-y-auto">
        <pre className="text-[var(--text-secondary)] whitespace-pre-wrap break-words">
          <code>{sanitizedScript}</code>
        </pre>
      </div>
    </div>
  );
};

export default ScriptBox;
