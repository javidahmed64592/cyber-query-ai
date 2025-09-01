"use client";

interface TextInputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  placeholder: string;
  buttonText: string;
  isLoading: boolean;
  loadingText?: string;
  multiline?: boolean;
  height?: string;
}

const TextInput = ({
  label,
  value,
  onChange,
  onSubmit,
  placeholder,
  buttonText,
  isLoading,
  loadingText = "Processing...",
  multiline = true,
  height = "h-32",
}: TextInputProps) => {
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
          {label}
        </label>
        {multiline ? (
          <textarea
            value={value}
            onChange={e => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            className={`cyber-input w-full ${height} resize-none`}
            disabled={isLoading}
          />
        ) : (
          <input
            type="text"
            value={value}
            onChange={e => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            className="cyber-input w-full"
            disabled={isLoading}
          />
        )}
      </div>

      <button
        onClick={onSubmit}
        disabled={isLoading || !value.trim()}
        className="cyber-button w-full sm:w-auto"
      >
        {isLoading ? (
          <span className="flex items-center justify-center space-x-2">
            <div className="animate-pulse-neon">⚡</div>
            <span>{loadingText}</span>
          </span>
        ) : (
          buttonText
        )}
      </button>
    </div>
  );
};

export default TextInput;
