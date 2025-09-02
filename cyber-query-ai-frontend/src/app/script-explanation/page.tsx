"use client";

import { useState } from "react";

import ExplanationBox from "@/components/ExplanationBox";
import LanguageSelector from "@/components/LanguageSelector";
import TextInput from "@/components/TextInput";
import { explainScript } from "@/lib/api";
import { sanitizeInput } from "@/lib/sanitization";
import { ExplanationResponse } from "@/lib/types";

export default function ScriptExplanation() {
  const [script, setScript] = useState("");
  const [language, setLanguage] = useState("python");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<ExplanationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!script.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await explainScript(sanitizeInput(script), language);
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setResponse(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold neon-glow text-[var(--text-primary)]">
          Script Explanation
        </h1>
        <p className="text-[var(--text-muted)] max-w-2xl mx-auto">
          Get detailed explanations of cybersecurity scripts. Understand what
          each line does, identify potential risks, and learn how scripts work
          for educational purposes.
        </p>
      </div>

      {/* Input Section */}
      <div className="max-w-4xl mx-auto space-y-6">
        <LanguageSelector
          value={language}
          onChange={setLanguage}
          disabled={isLoading}
        />

        <TextInput
          label="📜 Script Input:"
          value={script}
          onChange={setScript}
          onSubmit={handleSubmit}
          placeholder="Paste the script you want to understand... (Ctrl+Enter to submit)"
          buttonText="🚀 Explain Script"
          isLoading={isLoading}
          loadingText="Analyzing..."
          height="h-40"
        />
      </div>

      {/* Results Section */}
      {(isLoading || response || error) && (
        <div className="max-w-4xl mx-auto space-y-6">
          <hr className="border-[var(--terminal-border)]" />

          {/* Error Display */}
          {error && (
            <div className="terminal-border rounded-lg p-4 border-[var(--neon-red)]">
              <div className="text-[var(--neon-red)] font-medium">
                ❌ Error: {error}
              </div>
            </div>
          )}

          {/* Explanation */}
          <ExplanationBox
            explanation={response?.explanation || ""}
            isLoading={isLoading}
          />
        </div>
      )}

      {/* Welcome Message */}
      {!isLoading && !response && !error && (
        <div className="max-w-2xl mx-auto text-center space-y-4">
          <div className="text-[var(--text-muted)] text-lg">
            Understand any cybersecurity script! 📜
          </div>
          <div className="text-sm text-[var(--text-muted)] space-y-2">
            <p>Try explaining scripts like:</p>
            <ul className="space-y-1 text-left list-disc list-inside">
              <li>&quot;Python network scanner&quot;</li>
              <li>&quot;Bash privilege escalation checker&quot;</li>
              <li>&quot;PowerShell Active Directory enumeration&quot;</li>
              <li>&quot;JavaScript XSS payload generator&quot;</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
