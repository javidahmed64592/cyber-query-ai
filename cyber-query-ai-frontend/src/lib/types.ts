// TypeScript types matching FastAPI Pydantic models

// Request types
export interface PromptRequest {
  prompt: string;
}

export interface PromptWithLanguageRequest {
  prompt: string;
  language: string;
}

// Response types
export interface HealthResponse {
  status: string;
  timestamp: string;
}

export interface CommandGenerationResponse {
  commands: string[];
  explanation: string;
}

export interface ScriptGenerationResponse {
  script: string;
  explanation: string;
}

export interface ExplanationResponse {
  explanation: string;
}

export interface Exploit {
  title: string;
  link: string;
  description: string;
  severity: string;
}

export interface ExploitSearchResponse {
  attack_vector: string;
  exploits: Exploit[];
}

// UI State types
export interface CommandState {
  isLoading: boolean;
  response: CommandGenerationResponse | null;
  error: string | null;
}

// Component prop types
export interface CommandBoxProps {
  commands: string[];
  isLoading: boolean;
}

export interface ExplanationBoxProps {
  explanation: string;
  isLoading: boolean;
}

export interface PromptInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
}
