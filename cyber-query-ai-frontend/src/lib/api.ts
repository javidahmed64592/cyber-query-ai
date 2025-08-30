import axios from "axios";
import { PromptRequest, CommandGenerationResponse } from "./types";

// API client configuration
const api = axios.create({
  baseURL: "/api", // This will be proxied to localhost:8000/api
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
      throw new Error(
        error.response?.data?.detail || "Failed to generate command"
      );
    }
    throw new Error("Network error occurred");
  }
};

export default api;
