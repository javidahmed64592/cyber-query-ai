"use client";

import { useState } from "react";

import { useAuth } from "@/contexts/AuthContext";

export default function LoginPage() {
  const [apiKey, setApiKey] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!apiKey.trim()) {
      setError("Please enter an API key");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await login(apiKey);
      // Redirect is handled by AuthContext
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Login failed. Please check your API key."
      );
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--background)]">
      <div className="w-full max-w-md p-8 space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold neon-glow text-[var(--text-primary)]">
            CyberQueryAI
          </h1>
          <p className="text-[var(--text-muted)]">
            AI-powered cybersecurity assistant
          </p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label
              htmlFor="apiKey"
              className="block text-sm font-medium text-[var(--text-primary)]"
            >
              API Key
            </label>
            <input
              id="apiKey"
              type="password"
              value={apiKey}
              onChange={e => setApiKey(e.target.value)}
              placeholder="Enter your API key"
              disabled={isLoading}
              className="w-full px-4 py-3 bg-[var(--terminal-bg)] border border-[var(--terminal-border)] rounded-lg text-[var(--text-primary)] placeholder-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--neon-cyan)] disabled:opacity-50"
              autoComplete="off"
            />
          </div>

          {/* Error Display */}
          {error && (
            <div className="p-3 bg-[var(--terminal-bg)] border border-[var(--neon-red)] rounded-lg">
              <p className="text-sm text-[var(--neon-red)]">❌ {error}</p>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 px-4 bg-[var(--neon-cyan)] text-[var(--background)] font-medium rounded-lg hover:bg-opacity-80 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {isLoading ? "Authenticating..." : "Login"}
          </button>
        </form>

        {/* Help Text */}
        <div className="text-center space-y-2">
          <p className="text-xs text-[var(--text-muted)]">
            Your API key is stored locally and used to authenticate with the
            backend server.
          </p>
        </div>
      </div>
    </div>
  );
}
