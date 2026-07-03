"use client";

const Footer = () => {
  return (
    <footer className="fixed bottom-0 left-0 right-0 bg-background-secondary border-t border-terminal-border py-3 px-4 z-40">
      <div className="container mx-auto max-w-6xl">
        <div className="text-text-muted text-sm font-mono text-center flex flex-wrap justify-center gap-4">
          <span className="text-neon-green">cyber@query:~$</span>
          <span>ai</span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
