"use client";

import { version } from "../lib/version";

const Footer = () => {
  return (
    <footer className="fixed bottom-0 left-0 right-0 bg-[var(--background-secondary)] border-t border-[var(--terminal-border)] py-3 px-4 z-40">
      <div className="container mx-auto max-w-6xl">
        <div className="text-[var(--text-muted)] text-sm font-mono text-center flex flex-wrap justify-center gap-4">
          <span className="text-[var(--neon-green)]">cyber@query:~$</span>
          <span>--version v{version}</span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
