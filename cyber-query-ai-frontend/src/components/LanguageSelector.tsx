"use client";

interface LanguageSelectorProps {
  value: string;
  onChange: (language: string) => void;
  disabled?: boolean;
}

const LANGUAGES = [
  { value: "python", label: "🐍 Python" },
  { value: "bash", label: "🐚 Bash" },
  { value: "powershell", label: "💙 PowerShell" },
  { value: "javascript", label: "🟨 JavaScript" },
  { value: "go", label: "🐹 Go" },
  { value: "rust", label: "🦀 Rust" },
];

const LanguageSelector = ({
  value,
  onChange,
  disabled = false,
}: LanguageSelectorProps) => {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-[var(--text-primary)]">
        🧪 Select Language:
      </label>
      <select
        value={value}
        onChange={e => onChange(e.target.value)}
        disabled={disabled}
        className="cyber-input w-full sm:w-auto min-w-[200px]"
      >
        {LANGUAGES.map(lang => (
          <option key={lang.value} value={lang.value}>
            {lang.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;
