"use client";

import { sanitizeOutput, isCommandSafe } from "@/lib/sanitization";

interface CommandBoxProps {
  commands: string[];
  isLoading: boolean;
}

const CommandBox = ({ commands, isLoading }: CommandBoxProps) => {
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

          return (
            <div key={index} className="command-box group relative">
              <div className="flex items-center justify-between">
                <code className="text-[var(--text-secondary)] break-all flex-1 mr-2">
                  {sanitizedCommand}
                </code>
                {!safe && (
                  <div className="text-[var(--neon-red)] text-xs font-bold whitespace-nowrap flex-shrink-0">
                    ⚠️ POTENTIALLY UNSAFE
                  </div>
                )}
              </div>
              <button
                onClick={() => navigator.clipboard?.writeText(sanitizedCommand)}
                className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity
                           text-[var(--text-muted)] hover:text-[var(--text-primary)] text-sm"
                title="Copy to clipboard"
              >
                📋
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CommandBox;
