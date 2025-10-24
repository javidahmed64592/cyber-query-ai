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
              generate appropriate responses. You can interact with CyberQueryAI
              in two ways:
            </p>
            <div className="bg-[var(--background-secondary)] p-4 rounded border border-[var(--border-accent)]">
              <h3 className="font-semibold text-[var(--border-accent)] mb-2">
                🤖 AI Assistant (Recommended)
              </h3>
              <p className="mb-2">
                The <strong>AI Assistant</strong> is your primary interface for
                interacting with CyberQueryAI. It provides a conversational
                experience where you can ask questions, request commands or
                scripts, and get explanations - all in one place with full
                conversation history.
              </p>
              <p className="text-sm italic">
                Best for: General queries, learning, and interactive workflows
              </p>
            </div>
            <div className="bg-[var(--background-secondary)] p-4 rounded border border-[var(--terminal-border)]">
              <h3 className="font-semibold text-[var(--text-primary)] mb-2">
                🎯 Specialized Pages
              </h3>
              <p className="mb-2">
                For more specific tasks, you can use the dedicated pages:
              </p>
              <ul className="list-disc list-inside space-y-1 ml-4 text-sm">
                <li>
                  <strong>Command Generation:</strong> Focused interface for
                  generating CLI commands
                </li>
                <li>
                  <strong>Script Generation:</strong> Create scripts in specific
                  programming languages
                </li>
                <li>
                  <strong>Command Explanation:</strong> Get detailed breakdowns
                  of existing commands
                </li>
                <li>
                  <strong>Script Explanation:</strong> Understand how scripts
                  work line-by-line
                </li>
                <li>
                  <strong>Exploit Search:</strong> Research known
                  vulnerabilities for specific targets
                </li>
              </ul>
            </div>
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
                🤖 AI Assistant
              </h3>
              <p className="text-[var(--text-secondary)] text-sm">
                Interactive conversational interface with full chat history for
                natural, context-aware assistance with all cybersecurity tasks.
              </p>
            </div>
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

        {/* Security Policy Section */}
        <div className="terminal-border border-[var(--neon-red)] rounded-lg p-6 bg-red-950/20">
          <h2 className="text-2xl font-bold text-[var(--neon-red)] mb-4 flex items-center">
            ⚖️ Security Policy
          </h2>
          <div className="text-[var(--text-secondary)] space-y-4">
            <p>
              CyberQueryAI is a tool designed to support ethical cybersecurity
              research, penetration testing in controlled environments, and
              educational exploration. It leverages AI to generate commands,
              scripts, and insights that help users learn and work more
              efficiently.
            </p>
            <p className="text-[var(--neon-red)] font-semibold">
              By using this tool, you agree to the following:
            </p>
            <ul className="list-disc list-inside space-y-2 ml-4">
              <li>
                You will use CyberQueryAI{" "}
                <strong>only for ethical and legal purposes</strong>.
              </li>
              <li>
                You will not use this tool to perform or assist in{" "}
                <strong>unauthorized access</strong>,{" "}
                <strong>real-world exploitation</strong>, or{" "}
                <strong>harmful activities</strong>.
              </li>
              <li>
                You understand that all generated content should be{" "}
                <strong>verified for accuracy and safety</strong> before use.
              </li>
              <li>
                You accept full responsibility for how you apply the information
                generated by this tool.
              </li>
            </ul>
            <p>
              CyberQueryAI is intended to <strong>encourage learning</strong>,{" "}
              <strong>support responsible red teaming</strong>, and{" "}
              <strong>foster growth</strong> in cybersecurity skills. Misuse of
              this tool may have legal consequences and violates the spirit of
              ethical hacking.
            </p>
          </div>
        </div>

        {/* Important Reminders Section */}
        <div className="terminal-border border-[var(--border-accent)] rounded-lg p-6">
          <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-4 flex items-center">
            ⚠️ Important Reminders
          </h2>
          <div className="text-[var(--text-secondary)] space-y-4">
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
                Always follow responsible disclosure practices when discovering
                vulnerabilities.
              </li>
              <li>
                This tool is as smart as its training data. Always stay updated
                with the latest security practices.
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
