"use client";

import DOMPurify from "dompurify";
import { useState } from "react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

const ChatMessage = ({ role, content }: ChatMessageProps) => {
  const [copied, setCopied] = useState(false);

  const isUser = role === "user";

  // Sanitize content for safe rendering
  const sanitizedContent = DOMPurify.sanitize(content, {
    ALLOWED_TAGS: [
      "p",
      "br",
      "strong",
      "em",
      "code",
      "pre",
      "ul",
      "ol",
      "li",
      "h1",
      "h2",
      "h3",
      "h4",
      "h5",
      "h6",
    ],
    ALLOWED_ATTR: ["class"],
  });

  // Convert markdown-style code blocks to HTML
  const formatContent = (text: string): string => {
    // Replace code blocks with proper HTML
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    let formatted = text.replace(
      codeBlockRegex,
      (_, lang, code) =>
        `<pre><code class="language-${lang || "bash"}">${code.trim()}</code></pre>`
    );

    // Replace inline code
    formatted = formatted.replace(/`([^`]+)`/g, "<code>$1</code>");

    // Replace line breaks with <br>
    formatted = formatted.replace(/\n/g, "<br>");

    return formatted;
  };

  const formattedContent = formatContent(sanitizedContent);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error("Failed to copy:", error);
    }
  };

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4 group`}
    >
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 relative ${
          isUser
            ? "bg-[var(--border-accent)] text-white"
            : "bg-[var(--background-secondary)] border border-[var(--terminal-border)]"
        }`}
      >
        {/* Role indicator */}
        <div
          className={`text-xs font-semibold mb-1 ${
            isUser
              ? "text-white opacity-80"
              : "text-[var(--border-accent)] neon-glow"
          }`}
        >
          {isUser ? "You" : "CyberQueryAI"}
        </div>

        {/* Message content */}
        <div
          className={`prose prose-sm max-w-none ${
            isUser ? "text-white" : "text-[var(--text-primary)]"
          }`}
          dangerouslySetInnerHTML={{ __html: formattedContent }}
        />

        {/* Copy button */}
        {!isUser && (
          <button
            onClick={handleCopy}
            className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 p-1 rounded hover:bg-[var(--background-tertiary)] text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
            title="Copy message"
          >
            {copied ? (
              <svg
                className="w-4 h-4 text-green-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            ) : (
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                />
              </svg>
            )}
          </button>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
