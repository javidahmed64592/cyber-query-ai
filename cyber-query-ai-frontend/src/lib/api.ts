import axios from "axios";
import { useEffect, useState } from "react";

import type {
  PromptRequest,
  PromptWithLanguageRequest,
  CommandGenerationResponse,
  ScriptGenerationResponse,
  ExplanationResponse,
  ExploitSearchResponse,
  ConfigResponse,
  HealthResponse,
  ChatRequest,
  ChatResponse,
} from "@/lib/types";

// Determine the base URL based on environment
const getBaseURL = () => {
  if (typeof window === "undefined") return "";

  // In production static build, API is served from same origin
  if (process.env.NODE_ENV === "production") {
    return window.location.origin;
  }

  // In development, proxy to backend (handled by Next.js rewrites)
  return "";
};

// API client configuration
const api = axios.create({
  baseURL: getBaseURL() + "/api", // This will be proxied in dev, direct in production
  timeout: 30000, // 30 seconds timeout for LLM responses
  headers: {
    "Content-Type": "application/json",
  },
});

// Health status type
export type HealthStatus = "online" | "offline" | "checking";

// API functions
export const getHealth = async (): Promise<HealthResponse> => {
  try {
    const response = await api.get<HealthResponse>("/health");
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        const errorData = error.response.data;
        if (typeof errorData === "string") {
          throw new Error(errorData);
        } else if (errorData?.detail) {
          throw new Error(
            typeof errorData.detail === "string"
              ? errorData.detail
              : JSON.stringify(errorData.detail)
          );
        } else if (errorData?.message) {
          throw new Error(errorData.message);
        } else {
          throw new Error(
            `Server error: ${error.response.status} ${error.response.statusText}`
          );
        }
      } else if (error.request) {
        throw new Error(
          "No response from server. Please check if the backend is running."
        );
      } else {
        throw new Error(`Request failed: ${error.message}`);
      }
    }
    throw new Error("An unexpected error occurred");
  }
};

export const getConfig = async (): Promise<ConfigResponse> => {
  try {
    const response = await api.get<ConfigResponse>("/config");
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        const errorData = error.response.data;
        if (typeof errorData === "string") {
          throw new Error(errorData);
        } else if (errorData?.detail) {
          throw new Error(
            typeof errorData.detail === "string"
              ? errorData.detail
              : JSON.stringify(errorData.detail)
          );
        } else if (errorData?.message) {
          throw new Error(errorData.message);
        } else {
          throw new Error(
            `Server error: ${error.response.status} ${error.response.statusText}`
          );
        }
      } else if (error.request) {
        throw new Error(
          "No response from server. Please check if the backend is running."
        );
      } else {
        throw new Error(`Request failed: ${error.message}`);
      }
    }
    throw new Error("An unexpected error occurred");
  }
};

// Send chat message with conversation history
export const sendChatMessage = async (
  message: string,
  history: ChatRequest["history"]
): Promise<ChatResponse> => {
  const request: ChatRequest = { message, history };

  try {
    const response = await api.post<ChatResponse>("/chat", request);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        const errorData = error.response.data;
        if (typeof errorData === "string") {
          throw new Error(errorData);
        } else if (errorData?.detail) {
          throw new Error(
            typeof errorData.detail === "string"
              ? errorData.detail
              : JSON.stringify(errorData.detail)
          );
        } else if (errorData?.message) {
          throw new Error(errorData.message);
        } else {
          throw new Error(
            `Server error: ${error.response.status} ${error.response.statusText}`
          );
        }
      } else if (error.request) {
        throw new Error(
          "No response from server. Please check if the backend is running."
        );
      } else {
        throw new Error(`Request failed: ${error.message}`);
      }
    }
    throw new Error("An unexpected error occurred");
  }
};

// Generate command based on prompt
export const generateCommand = async (
  prompt: string
): Promise<CommandGenerationResponse> => {
  const request: PromptRequest = { prompt };

  try {
    const response = await api.post<CommandGenerationResponse>(
      "/generate-command",
      request
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // Handle different types of errors more specifically
      if (error.response) {
        // Server responded with error status
        const errorData = error.response.data;
        if (typeof errorData === "string") {
          throw new Error(errorData);
        } else if (errorData?.detail) {
          throw new Error(
            typeof errorData.detail === "string"
              ? errorData.detail
              : JSON.stringify(errorData.detail)
          );
        } else if (errorData?.message) {
          throw new Error(errorData.message);
        } else {
          throw new Error(
            `Server error: ${error.response.status} ${error.response.statusText}`
          );
        }
      } else if (error.request) {
        // Request was made but no response received
        throw new Error(
          "No response from server. Please check if the backend is running."
        );
      } else {
        // Something else happened
        throw new Error(`Request failed: ${error.message}`);
      }
    }
    throw new Error("An unexpected error occurred");
  }
};

// Generate script based on prompt and language
export const generateScript = async (
  prompt: string,
  language: string
): Promise<ScriptGenerationResponse> => {
  const request: PromptWithLanguageRequest = { prompt, language };

  try {
    const response = await api.post<ScriptGenerationResponse>(
      "/generate-script",
      request
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        const errorData = error.response.data;
        if (typeof errorData === "string") {
          throw new Error(errorData);
        } else if (errorData?.detail) {
          throw new Error(
            typeof errorData.detail === "string"
              ? errorData.detail
              : JSON.stringify(errorData.detail)
          );
        } else if (errorData?.message) {
          throw new Error(errorData.message);
        } else {
          throw new Error(
            `Server error: ${error.response.status} ${error.response.statusText}`
          );
        }
      } else if (error.request) {
        throw new Error(
          "No response from server. Please check if the backend is running."
        );
      } else {
        throw new Error(`Request failed: ${error.message}`);
      }
    }
    throw new Error("An unexpected error occurred");
  }
};

// Explain a command
export const explainCommand = async (
  command: string
): Promise<ExplanationResponse> => {
  const request: PromptRequest = { prompt: command };

  try {
    const response = await api.post<ExplanationResponse>(
      "/explain-command",
      request
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        const errorData = error.response.data;
        if (typeof errorData === "string") {
          throw new Error(errorData);
        } else if (errorData?.detail) {
          throw new Error(
            typeof errorData.detail === "string"
              ? errorData.detail
              : JSON.stringify(errorData.detail)
          );
        } else if (errorData?.message) {
          throw new Error(errorData.message);
        } else {
          throw new Error(
            `Server error: ${error.response.status} ${error.response.statusText}`
          );
        }
      } else if (error.request) {
        throw new Error(
          "No response from server. Please check if the backend is running."
        );
      } else {
        throw new Error(`Request failed: ${error.message}`);
      }
    }
    throw new Error("An unexpected error occurred");
  }
};

// Explain a script
export const explainScript = async (
  script: string,
  language: string
): Promise<ExplanationResponse> => {
  const request: PromptWithLanguageRequest = { prompt: script, language };

  try {
    const response = await api.post<ExplanationResponse>(
      "/explain-script",
      request
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        const errorData = error.response.data;
        if (typeof errorData === "string") {
          throw new Error(errorData);
        } else if (errorData?.detail) {
          throw new Error(
            typeof errorData.detail === "string"
              ? errorData.detail
              : JSON.stringify(errorData.detail)
          );
        } else if (errorData?.message) {
          throw new Error(errorData.message);
        } else {
          throw new Error(
            `Server error: ${error.response.status} ${error.response.statusText}`
          );
        }
      } else if (error.request) {
        throw new Error(
          "No response from server. Please check if the backend is running."
        );
      } else {
        throw new Error(`Request failed: ${error.message}`);
      }
    }
    throw new Error("An unexpected error occurred");
  }
};

// Search for exploits
export const searchExploits = async (
  targetDescription: string
): Promise<ExploitSearchResponse> => {
  const request: PromptRequest = { prompt: targetDescription };

  try {
    const response = await api.post<ExploitSearchResponse>(
      "/search-exploits",
      request
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        const errorData = error.response.data;
        if (typeof errorData === "string") {
          throw new Error(errorData);
        } else if (errorData?.detail) {
          throw new Error(
            typeof errorData.detail === "string"
              ? errorData.detail
              : JSON.stringify(errorData.detail)
          );
        } else if (errorData?.message) {
          throw new Error(errorData.message);
        } else {
          throw new Error(
            `Server error: ${error.response.status} ${error.response.statusText}`
          );
        }
      } else if (error.request) {
        throw new Error(
          "No response from server. Please check if the backend is running."
        );
      } else {
        throw new Error(`Request failed: ${error.message}`);
      }
    }
    throw new Error("An unexpected error occurred");
  }
};

// Health status hook
export function useHealthStatus(): HealthStatus {
  const [status, setStatus] = useState<HealthStatus>("checking");

  useEffect(() => {
    let isMounted = true;

    const checkHealth = async () => {
      try {
        const data = await getHealth();
        if (isMounted) {
          if (data.status === "healthy") {
            setStatus("online");
          } else {
            setStatus("offline");
          }
        }
      } catch {
        if (isMounted) {
          setStatus("offline");
        }
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // every 30s
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return status;
}

export default api;
