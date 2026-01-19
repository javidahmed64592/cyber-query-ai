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
        <label className="block text-sm font-medium text-text-primary mb-2">
          {label}
        </label>
        {multiline ? (
          <textarea
            value={value}
            onChange={e => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            className={`w-full ${height} resize-none bg-terminal-bg border border-terminal-border text-text-primary p-3 rounded-md font-mono transition-all duration-200 focus:outline-none focus:border-border-accent focus:shadow-[0_0_2px_#00ff41] disabled:opacity-50`}
            disabled={isLoading}
          />
        ) : (
          <input
            type="text"
            value={value}
            onChange={e => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            className="w-full bg-terminal-bg border border-terminal-border text-text-primary p-3 rounded-md font-mono transition-all duration-200 focus:outline-none focus:border-border-accent focus:shadow-[0_0_2px_#00ff41] disabled:opacity-50"
            disabled={isLoading}
          />
        )}
      </div>

      <button
        onClick={onSubmit}
        disabled={isLoading || !value.trim()}
        className="w-full sm:w-auto bg-background-secondary border border-border-accent text-text-primary px-6 py-3 rounded-md font-mono font-semibold cursor-pointer transition-all duration-200 uppercase tracking-wider hover:enabled:bg-border-accent hover:enabled:text-background hover:enabled:shadow-[0_0_2px_#00ff41] disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <span className="flex items-center justify-center space-x-2">
            <div className="animate-[pulse_2s_cubic-bezier(0.4,0,0.6,1)_infinite]">
              ⚡
            </div>
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
