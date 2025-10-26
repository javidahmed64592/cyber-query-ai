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
    version: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    message: str


class CodeGenerationResponse(BaseModel):
    """Response model for code generation."""

    code: str
    explanation: str
    language: str = "bash"


class CodeExplanationResponse(BaseModel):
    """Response model for code explanation endpoint."""

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
