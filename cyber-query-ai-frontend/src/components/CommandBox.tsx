"use client";

import { useState } from "react";

import { sanitizeOutput, isCommandSafe } from "@/lib/sanitization";

interface CommandBoxProps {
  commands: string[];
  isLoading: boolean;
}

const CommandBox = ({ commands, isLoading }: CommandBoxProps) => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const handleCopy = async (command: string, index: number) => {
    try {
      await navigator.clipboard?.writeText(command);
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    } catch {
      // Failed to copy to clipboard
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-[var(--text-primary)]">
          ✅ Generated Command(s):
        </h3>
        <div className="command-box animate-pulse-neon">
          <span className="text-[var(--text-muted)]">
            Generating commands...
          </span>
        </div>
      </div>
    );
  }

  if (commands.length === 0) {
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-[var(--text-primary)]">
          ✅ Generated Command(s):
        </h3>
        <div className="command-box">
          <span className="text-[var(--neon-red)]">
            No suitable tool identified. Try rephrasing your prompt.
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-[var(--text-primary)]">
        ✅ Generated Command(s):
      </h3>
      <div className="space-y-3">
        {commands.map((command, index) => {
          const sanitizedCommand = sanitizeOutput(command);
          const safe = isCommandSafe(sanitizedCommand);
          const isCopied = copiedIndex === index;

          return (
            <div key={index} className="command-box group relative">
              <div className="flex items-center justify-between">
                <code className="text-[var(--text-secondary)] break-all flex-1 mr-2">
                  {sanitizedCommand}
                </code>
                <div className="flex items-center gap-2 flex-shrink-0">
                  {!safe && (
                    <div className="text-[var(--neon-red)] text-xs font-bold whitespace-nowrap">
                      ⚠️ POTENTIALLY UNSAFE
                    </div>
                  )}
                  <button
                    onClick={() => handleCopy(sanitizedCommand, index)}
                    className="px-2 py-1 bg-[var(--surface-elevated)] hover:bg-[var(--surface-hover)]
                               border border-[var(--border-color)] rounded text-xs
                               text-[var(--text-muted)] hover:text-[var(--text-primary)]
                               transition-all duration-200 flex items-center gap-1"
                    title={isCopied ? "Copied!" : "Copy to clipboard"}
                  >
                    {isCopied ? "✓" : "📋"}
                    <span>{isCopied ? "Copied" : "Copy"}</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CommandBox;
