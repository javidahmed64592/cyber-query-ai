// TypeScript types matching FastAPI Pydantic models

// Base response types
export interface BaseResponse {
  code: number;
  message: string;
  timestamp: string;
}

// Request types
export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatRequest {
  message: string;
  history: ChatMessage[];
}

export interface PromptRequest {
  prompt: string;
}

// Authentication types
export interface LoginResponse extends BaseResponse {}

export interface AuthContextType {
  apiKey: string | null;
  isAuthenticated: boolean;
  login: (apiKey: string) => Promise<void>;
  logout: () => void;
}

// Response types
export interface HealthResponse extends BaseResponse {
  status: string;
}

export interface ModelConfig {
  model: string;
  embedding_model: string;
}

export interface ApiConfigResponse extends BaseResponse {
  model: ModelConfig;
  version: string;
}

export interface ChatResponse extends BaseResponse {
  model_message: string;
}

export interface CodeGenerationResponse extends BaseResponse {
  generated_code: string;
  explanation: string;
  language: string;
}

export interface CodeExplanationResponse extends BaseResponse {
  explanation: string;
}

export interface Exploit {
  title: string;
  link: string;
  severity: string;
  description: string;
}

export interface ExploitSearchResponse extends BaseResponse {
  exploits: Exploit[];
  explanation: string;
}

// UI State types
export interface CodeState {
  isLoading: boolean;
  response: CodeGenerationResponse | null;
  error: string | null;
}

// Component prop types
export interface CodeBoxProps {
  code: string;
  language: string;
  isLoading: boolean;
}

export interface ExplanationBoxProps {
  explanation: string;
  isLoading: boolean;
}
