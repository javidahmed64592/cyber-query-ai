"use client";

import { useState } from "react";

import ExplanationBox from "@/components/ExplanationBox";
import LanguageSelector from "@/components/LanguageSelector";
import ScriptBox from "@/components/ScriptBox";
import TextInput from "@/components/TextInput";
import { generateScript } from "@/lib/api";
import { sanitizeInput } from "@/lib/sanitization";
import { ScriptGenerationResponse } from "@/lib/types";

export default function ScriptGeneration() {
  const [prompt, setPrompt] = useState("");
  const [language, setLanguage] = useState("python");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<ScriptGenerationResponse | null>(
    null
  );
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!prompt.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await generateScript(sanitizeInput(prompt), language);
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
          Script Generation
        </h1>
        <p className="text-[var(--text-muted)] max-w-2xl mx-auto">
          Generate cybersecurity scripts in your preferred programming language
          for ethical penetration testing and security research. AI can make
          mistakes - please verify the generated scripts before use.
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
          label="🧠 Prompt:"
          value={prompt}
          onChange={setPrompt}
          onSubmit={handleSubmit}
          placeholder="Describe the script you want to generate... (Ctrl+Enter to submit)"
          buttonText="🚀 Generate Script"
          isLoading={isLoading}
          loadingText="Generating..."
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

          {/* Script Output */}
          <ScriptBox
            script={response?.script || ""}
            language={language}
            isLoading={isLoading}
          />

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
            Generate powerful cybersecurity scripts! 🐍
          </div>
          <div className="text-sm text-[var(--text-muted)] space-y-2">
            <p>Try asking for scripts like:</p>
            <ul className="space-y-1 text-left list-disc list-inside">
              <li>&quot;Create a port scanner in Python&quot;</li>
              <li>&quot;Write a password brute-forcer in Bash&quot;</li>
              <li>
                &quot;Generate a web crawler for vulnerability scanning&quot;
              </li>
              <li>&quot;Build a network packet analyzer&quot;</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
