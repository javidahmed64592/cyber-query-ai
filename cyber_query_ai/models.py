"""Data classes for the CyberQueryAI application."""

from pydantic import BaseModel


# Request schema
class PromptRequest(BaseModel):
    """Request model for command generation."""

    prompt: str


# Response schema
class CommandGenerationResponse(BaseModel):
    """Response model for command generation."""

    commands: list[str]
    explanation: str
