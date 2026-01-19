"use client";

import { sanitizeOutput } from "@/lib/sanitization";

interface ExplanationBoxProps {
  explanation: string;
  isLoading: boolean;
}

const INLINE_CODE_STYLE = {
  backgroundColor: "#1a1a1a",
  color: "#00ff41",
  padding: "0.125rem 0.375rem",
  borderRadius: "0.25rem",
  fontSize: "0.875em",
  fontFamily: "'Courier New', monospace",
  border: "1px solid #333333",
} as const;

const ExplanationBox = ({ explanation, isLoading }: ExplanationBoxProps) => {
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

  if (isLoading) {
    return (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-text-primary">
          📖 Explanation:
        </h3>
        <div className="border border-terminal-border bg-terminal-bg rounded-lg p-4 animate-[pulse_2s_cubic-bezier(0.4,0,0.6,1)_infinite]">
          <div className="text-text-muted">Generating explanation...</div>
        </div>
      </div>
    );
  }

  if (!explanation) {
    return null;
  }

  const sanitizedExplanation = sanitizeOutput(explanation);

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-text-primary">
        📖 Explanation:
      </h3>
      <div className="border border-terminal-border bg-terminal-bg rounded-lg p-4 max-h-64 overflow-y-auto">
        <div className="text-text-secondary whitespace-pre-wrap">
          {renderText(sanitizedExplanation)}
        </div>
      </div>
    </div>
  );
};

export default ExplanationBox;
