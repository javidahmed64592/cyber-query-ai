"use client";

import { useState } from "react";

import ExplanationBox from "@/components/ExplanationBox";
import ScriptBox from "@/components/ScriptBox";
import TextInput from "@/components/TextInput";
import { generateCode } from "@/lib/api";
import { sanitizeInput } from "@/lib/sanitization";
import { CodeGenerationResponse } from "@/lib/types";

export default function CodeGeneration() {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<CodeGenerationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!prompt.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await generateCode(sanitizeInput(prompt));
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
          Code Generation
        </h1>
        <p className="text-[var(--text-muted)] max-w-2xl mx-auto">
          Describe your cybersecurity task and get commands or scripts for
          ethical penetration testing and security research. The AI
          automatically determines whether to generate a simple command or a
          full script. AI can make mistakes - please verify the generated code
          before use.
        </p>
      </div>

      {/* Input Section */}
      <div className="max-w-4xl mx-auto">
        <TextInput
          label="🧠 Prompt:"
          value={prompt}
          onChange={setPrompt}
          onSubmit={handleSubmit}
          placeholder="Describe the task you want to perform... (Ctrl+Enter to submit)"
          buttonText="🚀 Generate Code"
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

          {/* Code Output */}
          <ScriptBox
            script={response?.code || ""}
            language={response?.language || "bash"}
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
            Welcome to CyberQueryAI! 🚀
          </div>
          <div className="text-sm text-[var(--text-muted)] space-y-2">
            <p>Try asking for code like:</p>
            <ul className="space-y-1 text-left list-disc list-inside">
              <li>&quot;Scan a network for open ports&quot;</li>
              <li>&quot;Write a Python script to crack MD5 hashes&quot;</li>
              <li>&quot;Perform a basic web vulnerability scan&quot;</li>
              <li>&quot;Extract metadata from image files&quot;</li>
              <li>&quot;Automate subdomain enumeration&quot;</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
