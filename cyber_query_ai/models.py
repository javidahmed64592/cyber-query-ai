"""Data classes for the CyberQueryAI application."""

from enum import StrEnum, auto

from pydantic import BaseModel, Field
from python_template_server.models import BaseResponse, TemplateServerConfig


# Application Server Configuration Models
class CyberQueryAIModelConfig(BaseModel):
    """Model configuration for the CyberQueryAI application."""

    model: str = Field(default="mistral", description="AI model to use for queries")
    embedding_model: str = Field(default="bge-m3", description="Embedding model to use")


class CyberQueryAIConfig(TemplateServerConfig):
    """Configuration settings for the CyberQueryAI application."""

    model: CyberQueryAIModelConfig = Field(default_factory=CyberQueryAIModelConfig, description="Model configuration")


# Request schemas
class RoleType(StrEnum):
    """Role types for chat messages."""

    USER = auto()
    ASSISTANT = auto()


class ChatMessage(BaseModel):
    """Chat message model for conversation history."""

    role: RoleType
    content: str


class PostChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str
    history: list[ChatMessage] = []


class PostPromptRequest(BaseModel):
    """Request model with prompt."""

    prompt: str


# Response schemas
class GetApiConfigResponse(BaseResponse):
    """Response model for API config endpoint."""

    model: CyberQueryAIModelConfig
    version: str


class PostChatResponse(BaseResponse):
    """Response model for chat endpoint."""

    model_message: str


class PostCodeGenerationResponse(BaseResponse):
    """Response model for code generation."""

    generated_code: str
    explanation: str
    language: str = "bash"


class PostCodeExplanationResponse(BaseResponse):
    """Response model for code explanation endpoint."""

    explanation: str


class Exploit(BaseModel):
    """Response model for exploit endpoint."""

    title: str
    link: str
    severity: str
    description: str


class PostExploitSearchResponse(BaseResponse):
    """Response model for exploit search endpoint."""

    exploits: list[Exploit]
    explanation: str
