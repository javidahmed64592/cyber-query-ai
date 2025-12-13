"use client";

import { useEffect, useState } from "react";

export interface ErrorNotificationProps {
  message: string;
  onClose: () => void;
  duration?: number;
}

export default function ErrorNotification({
  message,
  onClose,
  duration = 5000,
}: ErrorNotificationProps) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // Auto-close after duration
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(onClose, 300); // Wait for fade out animation
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const handleClose = () => {
    setIsVisible(false);
    setTimeout(onClose, 300); // Wait for fade out animation
  };

  return (
    <div
      className={`fixed top-4 right-4 z-50 max-w-md transition-all duration-300 ${
        isVisible ? "opacity-100 translate-x-0" : "opacity-0 translate-x-4"
      }`}
    >
      <div className="bg-[var(--terminal-bg)] border-2 border-[var(--neon-red)] rounded-lg shadow-lg p-4 flex items-start space-x-3">
        {/* Error Icon */}
        <div className="flex-shrink-0">
          <span className="text-2xl">❌</span>
        </div>

        {/* Error Content */}
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-semibold text-[var(--neon-red)] mb-1">
            Error
          </h3>
          <p className="text-sm text-[var(--text-primary)] break-words">
            {message}
          </p>
        </div>

        {/* Close Button */}
        <button
          onClick={handleClose}
          className="flex-shrink-0 text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors"
          aria-label="Close notification"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </div>
  );
}

/**
 * Hook for managing error notifications.
 */
export function useErrorNotification() {
  const [error, setError] = useState<string | null>(null);

  const showError = (message: string) => {
    setError(message);
  };

  const clearError = () => {
    setError(null);
  };

  return { error, showError, clearError };
}
