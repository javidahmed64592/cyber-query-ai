"use client";

import { useState } from "react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

interface ContentPart {
  type: "text" | "code";
  content: string;
  language?: string;
}

// Inline styles for code blocks (ChatGPT-inspired design)
const CODE_BLOCK_STYLES = {
  wrapper: {
    margin: "1rem 0",
    borderRadius: "0.5rem",
    overflow: "hidden",
    backgroundColor: "#0a0a0a",
    border: "1px solid #30363d",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "0.5rem 0.75rem",
    backgroundColor: "#1a1a1a",
    borderBottom: "1px solid #333333",
  },
  language: {
    fontSize: "0.75rem",
    fontWeight: 500,
    color: "#888888",
    textTransform: "lowercase" as const,
  },
  button: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "0.25rem",
    backgroundColor: "transparent",
    border: "none",
    borderRadius: "0.25rem",
    cursor: "pointer",
    transition: "color 0.2s",
  },
  pre: {
    margin: 0,
    padding: "1rem",
    overflowX: "auto" as const,
    backgroundColor: "#0a0a0a",
  },
  code: {
    fontFamily: "'Courier New', monospace",
    fontSize: "0.875rem",
    lineHeight: 1.5,
    color: "#00ff41",
    whiteSpace: "pre" as const,
  },
} as const;

const INLINE_CODE_STYLE = {
  backgroundColor: "#1a1a1a",
  color: "#00ff41",
  padding: "0.125rem 0.375rem",
  borderRadius: "0.25rem",
  fontSize: "0.875em",
  fontFamily: "'Courier New', monospace",
  border: "1px solid #333333",
} as const;

const ChatMessage = ({ role, content }: ChatMessageProps) => {
  const [copied, setCopied] = useState(false);
  const [copiedCodeBlock, setCopiedCodeBlock] = useState<number | null>(null);

  const isUser = role === "user";

  // Parse content into parts (text, code blocks, inline code)
  const parseContent = (text: string): ContentPart[] => {
    const parts: ContentPart[] = [];
    let currentIndex = 0;

    // Find all code blocks
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    let match;

    while ((match = codeBlockRegex.exec(text)) !== null) {
      // Add text before code block
      if (match.index > currentIndex) {
        const textContent = text.slice(currentIndex, match.index);
        if (textContent.trim()) {
          parts.push({ type: "text", content: textContent });
        }
      }

      // Add code block
      parts.push({
        type: "code",
        content: (match[2] || "").trim(),
        language: match[1] || "bash",
      });

      currentIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (currentIndex < text.length) {
      const textContent = text.slice(currentIndex);
      if (textContent.trim()) {
        parts.push({ type: "text", content: textContent });
      }
    }

    return parts;
  };

  const renderText = (text: string) => {
    // Handle inline code
    const inlineCodeRegex = /`([^`]+)`/g;
    const segments: (string | React.JSX.Element)[] = [];
    let lastIndex = 0;
    let match;

    while ((match = inlineCodeRegex.exec(text)) !== null) {
      // Add text before inline code
      if (match.index > lastIndex) {
        const textSegment = text.slice(lastIndex, match.index);
        segments.push(
          ...textSegment.split("\n").map((line, i) => (
            <span key={`text-${lastIndex}-${i}`}>
              {i > 0 && <br />}
              {line}
            </span>
          ))
        );
      }

      // Add inline code
      segments.push(
        <code key={`code-${match.index}`} style={INLINE_CODE_STYLE}>
          {match[1]}
        </code>
      );

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < text.length) {
      const textSegment = text.slice(lastIndex);
      segments.push(
        ...textSegment.split("\n").map((line, i) => (
          <span key={`text-${lastIndex}-${i}`}>
            {i > 0 && <br />}
            {line}
          </span>
        ))
      );
    }

    return segments;
  };

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

  const handleCodeBlockCopy = async (code: string, index: number) => {
    try {
      await navigator.clipboard.writeText(code);
      setCopiedCodeBlock(index);
      setTimeout(() => setCopiedCodeBlock(null), 2000);
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error("Failed to copy code:", error);
    }
  };

  const contentParts = parseContent(content);

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4 group`}
    >
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 relative ${
          isUser
            ? "bg-[#1a4d2e] text-neon-green border border-border-accent"
            : "bg-background-secondary border border-terminal-border"
        }`}
      >
        {/* Role indicator */}
        <div
          className={`text-xs font-semibold mb-1 ${
            isUser ? "text-neon-green opacity-90" : "text-border-accent"
          }`}
        >
          {isUser ? "You" : "CyberQueryAI"}
        </div>

        {/* Message content */}
        <div
          className={`prose prose-sm max-w-none ${
            isUser ? "text-neon-green" : "text-text-primary"
          }`}
        >
          {contentParts.map((part, index) => {
            if (part.type === "text") {
              return <div key={index}>{renderText(part.content)}</div>;
            } else if (part.type === "code") {
              const isCopied = copiedCodeBlock === index;
              return (
                <div key={index} style={CODE_BLOCK_STYLES.wrapper}>
                  {/* Code block header with language and copy button */}
                  <div style={CODE_BLOCK_STYLES.header}>
                    <span style={CODE_BLOCK_STYLES.language}>
                      {part.language}
                    </span>
                    <button
                      onClick={() => handleCodeBlockCopy(part.content, index)}
                      title="Copy code"
                      style={{
                        ...CODE_BLOCK_STYLES.button,
                        color: isCopied ? "#00ff41" : "#888888",
                      }}
                      onMouseEnter={e =>
                        !isCopied && (e.currentTarget.style.color = "#ffffff")
                      }
                      onMouseLeave={e =>
                        !isCopied && (e.currentTarget.style.color = "#888888")
                      }
                    >
                      {isCopied ? (
                        <svg
                          width="16"
                          height="16"
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
                          width="16"
                          height="16"
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
                  </div>

                  {/* Code content */}
                  <pre style={CODE_BLOCK_STYLES.pre}>
                    <code style={CODE_BLOCK_STYLES.code}>{part.content}</code>
                  </pre>
                </div>
              );
            }
            return null;
          })}
        </div>

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
