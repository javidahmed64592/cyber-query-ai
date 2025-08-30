import axios from "axios";

import { PromptRequest, CommandGenerationResponse } from "./types";

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

// API functions
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
          "No response from server. Please check if the backend is running on localhost:8000"
        );
      } else {
        // Something else happened
        throw new Error(`Request failed: ${error.message}`);
      }
    }
    throw new Error("An unexpected error occurred");
  }
};

export default api;
