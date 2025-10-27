// TypeScript types matching FastAPI Pydantic models

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

// Response types
export interface HealthResponse {
  status: string;
  timestamp: string;
}

export interface ConfigResponse {
  model: string;
  embedding_model: string;
  host: string;
  port: number;
  version: string;
}

export interface ChatResponse {
  message: string;
}

export interface CodeGenerationResponse {
  code: string;
  explanation: string;
  language: string;
}

export interface CodeExplanationResponse {
  explanation: string;
}

export interface Exploit {
  title: string;
  link: string;
  severity: string;
  description: string;
}

export interface ExploitSearchResponse {
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
