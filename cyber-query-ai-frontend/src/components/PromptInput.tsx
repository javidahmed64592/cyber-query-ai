"use client";

interface PromptInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
}

const PromptInput = ({
  value,
  onChange,
  onSubmit,
  isLoading,
}: PromptInputProps) => {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-2">
          🧠 Prompt:
        </label>
        <textarea
          value={value}
          onChange={e => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe the task you want to perform... (Ctrl+Enter to submit)"
          className="cyber-input w-full h-32 resize-none"
          disabled={isLoading}
        />
      </div>

      <button
        onClick={onSubmit}
        disabled={isLoading || !value.trim()}
        className="cyber-button w-full sm:w-auto"
      >
        {isLoading ? (
          <span className="flex items-center justify-center space-x-2">
            <div className="animate-pulse-neon">⚡</div>
            <span>Generating...</span>
          </span>
        ) : (
          "🚀 Generate Command"
        )}
      </button>
    </div>
  );
};

export default PromptInput;
