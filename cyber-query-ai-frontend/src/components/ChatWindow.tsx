"use client";

import { useEffect, useRef, useState } from "react";

import ChatMessage from "@/components/ChatMessage";
import ErrorNotification, {
  useErrorNotification,
} from "@/components/ErrorNotification";
import { sendChatMessage } from "@/lib/api";
import { sanitizeInput } from "@/lib/sanitization";
import type { ChatMessage as ChatMessageType } from "@/lib/types";

const ChatWindow = () => {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { error, showError, clearError } = useErrorNotification();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"; // Reset to auto to get accurate scrollHeight
      const scrollHeight = textareaRef.current.scrollHeight;
      const minHeight = 54; // Minimum height to match buttons
      const maxHeight = 54 * 4; // Max 4 rows (216px)
      textareaRef.current.style.height = `${Math.max(minHeight, Math.min(scrollHeight, maxHeight))}px`;
    }
  }, [input]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessageType = {
      role: "user",
      content: input,
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Send sanitized message with conversation history
      const response = await sendChatMessage(sanitizeInput(input), messages);

      // Add assistant response
      const assistantMessage: ChatMessageType = {
        role: "assistant",
        content: response.model_message,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to send message";
      showError(errorMessage);

      // Add error message to chat
      const errorChatMessage: ChatMessageType = {
        role: "assistant",
        content: `Error: ${errorMessage}`,
      };
      setMessages(prev => [...prev, errorChatMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClear = () => {
    setMessages([]);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Error Notification */}
      {error && <ErrorNotification message={error} onClose={clearError} />}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="text-6xl mb-4">💬</div>
            <h3 className="text-2xl font-bold text-text-primary mb-2">
              Welcome to CyberQueryAI
            </h3>
            <p className="text-text-secondary max-w-md">
              Ask me anything about cybersecurity tasks, and I&apos;ll help you
              generate commands, scripts, explanations, or search for exploits.
            </p>
            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl">
              <button
                onClick={() =>
                  setInput("How do I scan a network for open ports?")
                }
                className="p-3 text-left bg-background-secondary border border-terminal-border rounded hover:border-border-accent transition-colors duration-200"
              >
                <span className="text-text-secondary text-sm">Example:</span>
                <p className="text-text-primary mt-1">
                  How do I scan a network for open ports?
                </p>
              </button>
              <button
                onClick={() =>
                  setInput("Generate a Python script to brute force SSH")
                }
                className="p-3 text-left bg-background-secondary border border-terminal-border rounded hover:border-border-accent transition-colors duration-200"
              >
                <span className="text-text-secondary text-sm">Example:</span>
                <p className="text-text-primary mt-1">
                  Generate a Python script to brute force SSH
                </p>
              </button>
              <button
                onClick={() => setInput("Explain how SQL injection works")}
                className="p-3 text-left bg-background-secondary border border-terminal-border rounded hover:border-border-accent transition-colors duration-200"
              >
                <span className="text-text-secondary text-sm">Example:</span>
                <p className="text-text-primary mt-1">
                  Explain how SQL injection works
                </p>
              </button>
              <button
                onClick={() =>
                  setInput("Search for Apache Struts vulnerabilities")
                }
                className="p-3 text-left bg-background-secondary border border-terminal-border rounded hover:border-border-accent transition-colors duration-200"
              >
                <span className="text-text-secondary text-sm">Example:</span>
                <p className="text-text-primary mt-1">
                  Search for Apache Struts vulnerabilities
                </p>
              </button>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                role={message.role}
                content={message.content}
              />
            ))}
            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="bg-background-secondary border border-terminal-border rounded-lg px-4 py-3">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-border-accent rounded-full animate-pulse" />
                    <div
                      className="w-2 h-2 bg-border-accent rounded-full animate-pulse"
                      style={{ animationDelay: "0.2s" }}
                    />
                    <div
                      className="w-2 h-2 bg-border-accent rounded-full animate-pulse"
                      style={{ animationDelay: "0.4s" }}
                    />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-terminal-border bg-background-secondary">
        <div className="flex items-end space-x-3">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Ask me anything about cybersecurity..."
            disabled={isLoading}
            className="flex-1 bg-terminal-bg border border-terminal-border text-text-primary p-3 rounded-md font-mono transition-all duration-200 focus:outline-none focus:border-border-accent focus:shadow-[0_0_2px_#00ff41] disabled:opacity-50 resize-none overflow-y-auto"
            rows={1}
            style={{ minHeight: "54px", maxHeight: "216px" }}
          />
          <button
            onClick={handleClear}
            disabled={messages.length === 0 || isLoading}
            className="p-3 bg-background-tertiary border border-terminal-border text-text-secondary rounded hover:enabled:bg-terminal-border hover:enabled:text-text-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 h-[54px] w-[54px] flex items-center justify-center"
            title="Clear chat history"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="p-3 bg-border-accent text-white rounded hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity duration-200 h-[54px] w-[54px] flex items-center justify-center"
            title={isLoading ? "Sending..." : "Send message"}
          >
            {isLoading ? (
              <svg
                className="w-5 h-5 animate-spin"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
            ) : (
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                />
              </svg>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
