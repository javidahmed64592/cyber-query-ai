"""Data classes for the CyberQueryAI application."""

from pydantic import BaseModel


# Request schemas
class PromptRequest(BaseModel):
    """Request model with prompt."""

    prompt: str


class PromptWithLanguageRequest(BaseModel):
    """Request model with prompt and language."""

    prompt: str
    language: str


# Response schemas
class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    timestamp: str


class CommandGenerationResponse(BaseModel):
    """Response model for command generation."""

    commands: list[str]
    explanation: str


class ScriptGenerationResponse(BaseModel):
    """Response model for script generation."""

    script: str
    explanation: str


class ExplanationResponse(BaseModel):
    """Response model for explanation."""

    explanation: str


class Exploit(BaseModel):
    """Response model for exploit."""

    title: str
    link: str
    severity: str
    description: str


class ExploitSearchResponse(BaseModel):
    """Response model for exploit search."""

    exploits: list[Exploit]
    explanation: str
