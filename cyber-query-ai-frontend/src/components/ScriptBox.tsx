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
        <h3 className="text-lg font-semibold text-text-primary">
          📜 Generated Script:
        </h3>
        <div className="bg-terminal-bg border border-terminal-border rounded-lg p-4 font-mono text-text-secondary relative overflow-x-auto animate-[pulse_2s_cubic-bezier(0.4,0,0.6,1)_infinite]">
          <span className="text-text-muted">Generating script...</span>
        </div>
      </div>
    );
  }

  if (!script) {
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-text-primary">
          📜 Generated Script:
        </h3>
        <div className="bg-terminal-bg border border-terminal-border rounded-lg p-4 font-mono text-text-secondary relative overflow-x-auto">
          <span className="text-neon-red">
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
        <h3 className="text-lg font-semibold text-text-primary">
          📜 Generated Script ({language}):
        </h3>
        <button
          onClick={handleCopy}
          className="px-3 py-2 bg-background-tertiary hover:bg-terminal-border
                     border border-border rounded text-sm
                     text-text-muted hover:text-text-primary
                     transition-all duration-200 flex items-center gap-2"
          title={isCopied ? "Copied!" : "Copy to clipboard"}
        >
          {isCopied ? "✓" : "📋"}
          <span>{isCopied ? "Copied" : "Copy Script"}</span>
        </button>
      </div>
      <div className="bg-terminal-bg border border-terminal-border rounded-lg p-4 font-mono text-text-secondary relative overflow-x-auto max-h-96 overflow-y-auto">
        <pre className="text-text-secondary whitespace-pre-wrap break-words">
          <code>{sanitizedScript}</code>
        </pre>
      </div>
    </div>
  );
};

export default ScriptBox;
