"""API router for the CyberQueryAI application."""

import json
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from slowapi import Limiter

from cyber_query_ai.helpers import clean_json_response, sanitize_dictionary, sanitize_text
from cyber_query_ai.models import CommandGenerationResponse, HealthResponse, PromptRequest

LIMITER_INTERVAL = "5/minute"

api_router = APIRouter(prefix="/api")
limiter = Limiter(key_func=lambda request: request.client.host)


def get_api_router() -> APIRouter:
    """Get the API router."""
    return api_router


def get_limiter() -> Limiter:
    """Get the rate limiter."""
    return limiter


def get_server_error(error: str, exception: Exception, response_text: str | None) -> HTTPException:
    """Handle generic server errors."""
    return HTTPException(
        status_code=500,
        detail={
            "error": error,
            "details": f"{exception!s}",
            "raw": str(response_text) if response_text else "No response",
        },
    )


@api_router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check the health of the server."""
    return HealthResponse(status="healthy", timestamp=datetime.now().isoformat() + "Z")


@api_router.post("/generate-command", response_model=CommandGenerationResponse)
@limiter.limit(LIMITER_INTERVAL)
async def generate_command(request: Request, prompt: PromptRequest) -> CommandGenerationResponse:
    """Generate cybersecurity commands based on user prompt."""
    chatbot = request.app.state.chatbot
    formatted_prompt = sanitize_text(chatbot.prompt_command_generation(task=prompt.prompt))
    response_text = None

    try:
        response_text = clean_json_response(await run_in_threadpool(chatbot.llm, formatted_prompt))
        parsed = json.loads(response_text)

        if missing_keys := set(CommandGenerationResponse.model_fields) - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            return CommandGenerationResponse(commands=[], explanation=msg)

        return CommandGenerationResponse(**sanitize_dictionary(parsed))
    except json.JSONDecodeError as e:
        msg = "Invalid JSON response from LLM"
        raise get_server_error(msg, e, response_text) from e
    except Exception as e:
        msg = "Failed to generate or parse LLM response"
        raise get_server_error(msg, e, response_text) from e
