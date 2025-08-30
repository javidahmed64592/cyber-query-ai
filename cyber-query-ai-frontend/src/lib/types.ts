// TypeScript types matching FastAPI Pydantic models

// Request types
export interface PromptRequest {
  prompt: string;
}

// Response types
export interface CommandGenerationResponse {
  commands: string[];
  explanation: string;
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
