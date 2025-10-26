"use client";

import { useState } from "react";

import ExplanationBox from "@/components/ExplanationBox";
import TextInput from "@/components/TextInput";
import { explainCode } from "@/lib/api";
import { sanitizeInput } from "@/lib/sanitization";
import { CodeExplanationResponse } from "@/lib/types";

export default function CodeExplanation() {
  const [code, setCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<CodeExplanationResponse | null>(
    null
  );
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!code.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await explainCode(sanitizeInput(code));
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
          Code Explanation
        </h1>
        <p className="text-[var(--text-muted)] max-w-2xl mx-auto">
          Get detailed explanations of cybersecurity commands and scripts.
          Understand what each part does and learn how to use tools effectively
          for ethical penetration testing. The AI automatically detects the
          language from your code.
        </p>
      </div>

      {/* Input Section */}
      <div className="max-w-4xl mx-auto">
        <TextInput
          label="🔍 Code Input:"
          value={code}
          onChange={setCode}
          onSubmit={handleSubmit}
          placeholder="Enter the command or script you want to understand... (Ctrl+Enter to submit)"
          buttonText="🚀 Explain Code"
          isLoading={isLoading}
          loadingText="Analyzing..."
          multiline={true}
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
            Understand any cybersecurity code! 🔍
          </div>
          <div className="text-sm text-[var(--text-muted)] space-y-2">
            <p>Try explaining code like:</p>
            <ul className="space-y-1 text-left list-disc list-inside">
              <li>&quot;nmap -sS -O 192.168.1.0/24&quot;</li>
              <li>&quot;john --wordlist=rockyou.txt hashes.txt&quot;</li>
              <li>&quot;Python script for brute forcing SSH&quot;</li>
              <li>&quot;Bash script for subdomain enumeration&quot;</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
