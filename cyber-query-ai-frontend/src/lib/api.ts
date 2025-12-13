import axios from "axios";
import { useEffect, useState } from "react";

import { getApiKey } from "@/lib/auth";
import type {
  PromptRequest,
  CodeGenerationResponse,
  CodeExplanationResponse,
  ExploitSearchResponse,
  ApiConfigResponse,
  HealthResponse,
  ChatRequest,
  ChatResponse,
  LoginResponse,
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

// Add request interceptor to include API key
api.interceptors.request.use(
  config => {
    const apiKey = getApiKey();
    if (apiKey) {
      config.headers["X-API-KEY"] = apiKey;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Health status type
export type HealthStatus = "online" | "offline" | "checking";

const extractErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      const errorData = error.response.data;

      // Check for BaseResponse format with message field
      if (errorData?.message) {
        return errorData.message;
      }

      // Check for detail field (common in FastAPI errors)
      if (errorData?.detail) {
        return typeof errorData.detail === "string"
          ? errorData.detail
          : JSON.stringify(errorData.detail);
      }

      // Fallback to generic server error
      return `Server error: ${error.response.status} ${error.response.statusText}`;
    } else if (error.request) {
      return "No response from server. Please check if the backend is running.";
    } else {
      return `Request failed: ${error.message}`;
    }
  }
  return "An unexpected error occurred";
};

const isSuccessResponse = (data: { code?: number }): boolean => {
  return data.code !== undefined && data.code >= 200 && data.code < 300;
};

// API functions
export const getHealth = async (): Promise<HealthResponse> => {
  try {
    const response = await api.get<HealthResponse>("/health");
    return response.data;
  } catch (error) {
    throw new Error(extractErrorMessage(error));
  }
};

export const getConfig = async (): Promise<ApiConfigResponse> => {
  try {
    const response = await api.get<ApiConfigResponse>("/config");
    const data = response.data;

    if (!isSuccessResponse(data)) {
      throw new Error(data.message || "Failed to get configuration");
    }

    return data;
  } catch (error) {
    throw new Error(extractErrorMessage(error));
  }
};

export const login = async (apiKey: string): Promise<LoginResponse> => {
  try {
    const response = await api.post<LoginResponse>(
      "/login",
      {},
      {
        headers: {
          "X-API-KEY": apiKey,
        },
      }
    );
    const data = response.data;

    if (!isSuccessResponse(data)) {
      throw new Error(data.message || "Login failed");
    }

    return data;
  } catch (error) {
    throw new Error(extractErrorMessage(error));
  }
};

// Send chat message with conversation history
export const sendChatMessage = async (
  message: string,
  history: ChatRequest["history"]
): Promise<ChatResponse> => {
  const request: ChatRequest = { message, history };

  try {
    const response = await api.post<ChatResponse>("/model/chat", request);
    const data = response.data;

    if (!isSuccessResponse(data)) {
      throw new Error(data.message || "Failed to send chat message");
    }

    return data;
  } catch (error) {
    throw new Error(extractErrorMessage(error));
  }
};

// Generate code (commands or scripts) based on prompt
export const generateCode = async (
  prompt: string
): Promise<CodeGenerationResponse> => {
  const request: PromptRequest = { prompt };

  try {
    const response = await api.post<CodeGenerationResponse>(
      "/code/generate",
      request
    );
    const data = response.data;

    if (!isSuccessResponse(data)) {
      throw new Error(data.message || "Failed to generate code");
    }

    return data;
  } catch (error) {
    throw new Error(extractErrorMessage(error));
  }
};

// Explain code (commands or scripts)
export const explainCode = async (
  code: string
): Promise<CodeExplanationResponse> => {
  const request: PromptRequest = { prompt: code };

  try {
    const response = await api.post<CodeExplanationResponse>(
      "/code/explain",
      request
    );
    const data = response.data;

    if (!isSuccessResponse(data)) {
      throw new Error(data.message || "Failed to explain code");
    }

    return data;
  } catch (error) {
    throw new Error(extractErrorMessage(error));
  }
};

// Search for exploits
export const searchExploits = async (
  targetDescription: string
): Promise<ExploitSearchResponse> => {
  const request: PromptRequest = { prompt: targetDescription };

  try {
    const response = await api.post<ExploitSearchResponse>(
      "/exploit/search",
      request
    );
    const data = response.data;

    if (!isSuccessResponse(data)) {
      throw new Error(data.message || "Failed to search exploits");
    }

    return data;
  } catch (error) {
    throw new Error(extractErrorMessage(error));
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
