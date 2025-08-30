'use client';

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
          <div className="text-[var(--text-muted)]">
            Generating commands...
          </div>
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
          <div className="text-[var(--neon-red)]">
            No suitable tool identified. Try rephrasing your prompt.
          </div>
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
        {commands.map((command, index) => (
          <div key={index} className="command-box group relative">
            <code className="text-[var(--text-secondary)] break-all">
              {command}
            </code>
            <button
              onClick={() => navigator.clipboard?.writeText(command)}
              className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity
                         text-[var(--text-muted)] hover:text-[var(--text-primary)] text-sm"
              title="Copy to clipboard"
            >
              📋
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CommandBox;
