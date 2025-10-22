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
    """Response model for health check endpoint."""

    status: str
    timestamp: str


class ConfigResponse(BaseModel):
    """Response model for config endpoint."""

    host: str
    port: int


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
