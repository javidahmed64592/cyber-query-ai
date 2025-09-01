"use client";

export default function About() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold neon-glow text-[var(--text-primary)]">
          About CyberQueryAI
        </h1>
        <p className="text-[var(--text-muted)] max-w-2xl mx-auto">
          Your AI-powered cybersecurity assistant for ethical hacking and
          security research.
        </p>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto space-y-8">
        {/* About Section */}
        <div className="terminal-border rounded-lg p-6">
          <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-4 flex items-center">
            🧠 About CyberQueryAI
          </h2>
          <div className="text-[var(--text-secondary)] space-y-4">
            <p>
              CyberQueryAI is an advanced AI-powered platform designed to assist
              cybersecurity professionals, researchers, and ethical hackers in
              their security assessment activities. This tool leverages
              state-of-the-art language models to generate commands, scripts,
              and explanations for various cybersecurity tasks.
            </p>
            <p>
              Whether you&apos;re conducting authorized penetration tests,
              learning about security tools, or researching vulnerabilities,
              CyberQueryAI provides intelligent assistance to help you work more
              efficiently and understand complex security concepts.
            </p>
          </div>
        </div>

        {/* How It Works Section */}
        <div className="terminal-border rounded-lg p-6">
          <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-4 flex items-center">
            💡 How It Works
          </h2>
          <div className="text-[var(--text-secondary)] space-y-4">
            <p>
              This tool uses advanced AI models to understand your requests and
              generate appropriate responses:
            </p>
            <ul className="list-disc list-inside space-y-2 ml-4">
              <li>
                <strong>Command Generation:</strong> Converts natural language
                descriptions into precise CLI commands for security tools like
                nmap, metasploit, john, and more.
              </li>
              <li>
                <strong>Script Generation:</strong> Creates custom scripts in
                various programming languages (Python, Bash, PowerShell, etc.)
                for specific security tasks.
              </li>
              <li>
                <strong>Explanations:</strong> Provides detailed breakdowns of
                commands and scripts to help you understand how they work.
              </li>
              <li>
                <strong>Exploit Research:</strong> Suggests known
                vulnerabilities and attack vectors based on target descriptions.
              </li>
            </ul>
            <p>
              All outputs are sanitized and filtered to promote safe and ethical
              usage patterns.
            </p>
          </div>
        </div>

        {/* Features Section */}
        <div className="terminal-border rounded-lg p-6">
          <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-4 flex items-center">
            🚀 Features
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h3 className="font-semibold text-[var(--border-accent)]">
                🛠️ Command Generation
              </h3>
              <p className="text-[var(--text-secondary)] text-sm">
                Generate CLI commands for network scanning, vulnerability
                assessment, and penetration testing tools.
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold text-[var(--border-accent)]">
                📜 Script Creation
              </h3>
              <p className="text-[var(--text-secondary)] text-sm">
                Create custom scripts in multiple programming languages for
                automated security tasks.
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold text-[var(--border-accent)]">
                🔍 Command Analysis
              </h3>
              <p className="text-[var(--text-secondary)] text-sm">
                Understand complex commands with detailed explanations of
                parameters and functionality.
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold text-[var(--border-accent)]">
                🧨 Exploit Research
              </h3>
              <p className="text-[var(--text-secondary)] text-sm">
                Discover known vulnerabilities and attack vectors for specific
                targets and technologies.
              </p>
            </div>
          </div>
        </div>

        {/* Disclaimer Section */}
        <div className="terminal-border border-[var(--neon-red)] rounded-lg p-6 bg-red-950/20">
          <h2 className="text-2xl font-bold text-[var(--neon-red)] mb-4 flex items-center">
            ⚠️ Important Disclaimer
          </h2>
          <div className="text-[var(--text-secondary)] space-y-4">
            <p className="text-[var(--neon-red)] font-semibold">
              This tool is intended for educational purposes and authorized
              security testing only.
            </p>
            <ul className="list-disc list-inside space-y-2 ml-4">
              <li>
                Always verify AI-generated content before use - language models
                can make mistakes or provide outdated information.
              </li>
              <li>
                Only use these tools and techniques on systems you own or have
                explicit written permission to test.
              </li>
              <li>
                Unauthorized access to computer systems is illegal and
                unethical.
              </li>
              <li>I am not responsible for misuse of this tool.</li>
              <li>
                Always follow responsible disclosure practices when discovering
                vulnerabilities.
              </li>
              <li>
                This tool is as smart as its training data. Always stay updated
                with the latest security practices.
              </li>
            </ul>
            <p>
              By using this tool, you agree to use it responsibly and in
              compliance with all applicable laws and regulations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
