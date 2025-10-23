"""Data classes for the CyberQueryAI application."""

from pydantic import BaseModel


# Request schemas
class ChatMessage(BaseModel):
    """Chat message model for conversation history."""

    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str
    history: list[ChatMessage] = []


class PromptRequest(BaseModel):
    """Request model with prompt."""

    prompt: str


class PromptWithLanguageRequest(BaseModel):
    """Request model with prompt and language."""

    prompt: str
    language: str


# Response schemas
class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str
    timestamp: str


class ConfigResponse(BaseModel):
    """Configuration settings for the CyberQueryAI application."""

    model: str
    embedding_model: str
    host: str
    port: int


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    message: str


class CommandGenerationResponse(BaseModel):
    """Response model for command generation endpoint."""

    commands: list[str]
    explanation: str


class ScriptGenerationResponse(BaseModel):
    """Response model for script generation endpoint."""

    script: str
    explanation: str


class ExplanationResponse(BaseModel):
    """Response model for explanation endpoint."""

    explanation: str


class Exploit(BaseModel):
    """Response model for exploit endpoint."""

    title: str
    link: str
    severity: str
    description: str


class ExploitSearchResponse(BaseModel):
    """Response model for exploit search endpoint."""

    exploits: list[Exploit]
    explanation: str
