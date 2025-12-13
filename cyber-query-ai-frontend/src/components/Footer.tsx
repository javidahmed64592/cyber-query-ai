"use client";

import { useState, useEffect } from "react";

import { getConfig } from "@/lib/api";
import type { ApiConfigResponse } from "@/lib/types";

const Footer = () => {
  const [config, setConfig] = useState<ApiConfigResponse | null>(null);

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const configData = await getConfig();
        setConfig(configData);
      } catch (error) {
        // Silently fail - footer will just show version without models
        // Error logged for debugging purposes only
        if (process.env.NODE_ENV === "development") {
          // eslint-disable-next-line no-console
          console.error("Failed to fetch config:", error);
        }
      }
    };

    fetchConfig();
  }, []);

  return (
    <footer className="fixed bottom-0 left-0 right-0 bg-[var(--background-secondary)] border-t border-[var(--terminal-border)] py-3 px-4 z-40">
      <div className="container mx-auto max-w-6xl">
        <div className="text-[var(--text-muted)] text-sm font-mono text-center flex flex-wrap justify-center gap-4">
          <span className="text-[var(--neon-green)]">cyber@query:~$</span>
          {config ? (
            <>
              <span>--version v{config.version}</span>
              <span className="text-[var(--terminal-border)]">|</span>
              <span>--model {config.model.model}</span>
              <span className="text-[var(--terminal-border)]">|</span>
              <span>--rag_model {config.model.embedding_model}</span>
            </>
          ) : (
            <span>--loading...</span>
          )}
        </div>
      </div>
    </footer>
  );
};

export default Footer;
