"use client";

import { useState } from "react";

import ExplanationBox from "@/components/ExplanationBox";
import TextInput from "@/components/TextInput";
import { explainCommand } from "@/lib/api";
import { sanitizeInput } from "@/lib/sanitization";
import { ExplanationResponse } from "@/lib/types";

export default function CommandExplanation() {
  const [command, setCommand] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<ExplanationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!command.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await explainCommand(sanitizeInput(command));
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
          Command Explanation
        </h1>
        <p className="text-[var(--text-muted)] max-w-2xl mx-auto">
          Get detailed explanations of cybersecurity CLI commands. Understand
          what each parameter does and learn how to use tools effectively for
          ethical penetration testing.
        </p>
      </div>

      {/* Input Section */}
      <div className="max-w-4xl mx-auto">
        <TextInput
          label="🔍 Command Input:"
          value={command}
          onChange={setCommand}
          onSubmit={handleSubmit}
          placeholder="Enter the CLI command you want to understand... (Ctrl+Enter to submit)"
          buttonText="🚀 Explain Command"
          isLoading={isLoading}
          loadingText="Analyzing..."
          multiline={false}
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
            Understand any cybersecurity command! 🔍
          </div>
          <div className="text-sm text-[var(--text-muted)] space-y-2">
            <p>Try explaining commands like:</p>
            <ul className="space-y-1 text-left list-disc list-inside">
              <li>&quot;nmap -sS -O 192.168.1.0/24&quot;</li>
              <li>&quot;john --wordlist=rockyou.txt hashes.txt&quot;</li>
              <li>&quot;hydra -l admin -P passwords.txt ssh://target&quot;</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
