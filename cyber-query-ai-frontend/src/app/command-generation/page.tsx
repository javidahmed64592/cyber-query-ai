'use client';

import { useState } from 'react';
import PromptInput from '@/components/PromptInput';
import CommandBox from '@/components/CommandBox';
import ExplanationBox from '@/components/ExplanationBox';
import { generateCommand } from '@/lib/api';
import { CommandGenerationResponse } from '@/lib/types';

export default function CommandGeneration() {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<CommandGenerationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!prompt.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await generateCommand(prompt);
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
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
          Command Generation
        </h1>
        <p className="text-[var(--text-muted)] max-w-2xl mx-auto">
          Describe your cybersecurity task and get precise CLI commands for ethical
          penetration testing and security research. AI can make mistakes - please
          verify the generated commands before use.
        </p>
      </div>

      {/* Input Section */}
      <div className="max-w-4xl mx-auto">
        <PromptInput
          value={prompt}
          onChange={setPrompt}
          onSubmit={handleSubmit}
          isLoading={isLoading}
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

          {/* Command Output */}
          <CommandBox
            commands={response?.commands || []}
            isLoading={isLoading}
          />

          {/* Explanation */}
          <ExplanationBox
            explanation={response?.explanation || ''}
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
            <p>Try asking for commands like:</p>
            <ul className="space-y-1 text-left list-disc list-inside">
              <li>&quot;Scan a network for open ports&quot;</li>
              <li>&quot;Crack an MD5 hash using a dictionary attack&quot;</li>
              <li>&quot;Perform a basic web vulnerability scan&quot;</li>
              <li>&quot;Extract metadata from an image file&quot;</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
