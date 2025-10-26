"""API router for the CyberQueryAI application."""

import json
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from slowapi import Limiter

from cyber_query_ai.helpers import clean_json_response, sanitize_text
from cyber_query_ai.models import (
    ChatRequest,
    ChatResponse,
    CodeExplanationResponse,
    CodeGenerationResponse,
    ConfigResponse,
    ExploitSearchResponse,
    HealthResponse,
    PromptRequest,
)

API_PREFIX = "/api"
LIMITER_INTERVAL = "5/minute"

api_router = APIRouter(prefix=API_PREFIX)
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
async def get_health() -> HealthResponse:
    """Check the health of the server."""
    return HealthResponse(status="healthy", timestamp=datetime.now().isoformat() + "Z")


@api_router.get("/config", response_model=ConfigResponse)
async def get_config(request: Request) -> ConfigResponse:
    """Get the server configuration."""
    config: ConfigResponse = request.app.state.config
    return config


@api_router.post("/chat", response_model=ChatResponse)
@limiter.limit(LIMITER_INTERVAL)
async def chat(request: Request, chat_request: ChatRequest) -> ChatResponse:
    """Chat with the AI assistant using conversation history."""
    chatbot = request.app.state.chatbot

    history_text = ""
    for msg in chat_request.history:
        role = "User" if msg.role == "user" else "Assistant"
        history_text += f"{role}: {msg.content}\n"

    formatted_prompt = sanitize_text(chatbot.prompt_chat(chat_request.message, history_text))
    response_text = None

    try:
        response_text = await run_in_threadpool(chatbot.llm.invoke, formatted_prompt)
        return ChatResponse(message=sanitize_text(response_text))
    except Exception as e:
        error_msg = "Failed to generate chat response"
        raise get_server_error(error_msg, e, response_text) from e


@api_router.post("/generate-code", response_model=CodeGenerationResponse)
@limiter.limit(LIMITER_INTERVAL)
async def generate_code(request: Request, prompt_request: PromptRequest) -> CodeGenerationResponse:
    """Generate cybersecurity code based on user prompt.

    The LLM automatically infers the appropriate language (bash, python, powershell, etc.)
    based on the task description.
    """
    chatbot = request.app.state.chatbot
    formatted_prompt = sanitize_text(chatbot.prompt_code_generation(prompt_request.prompt))
    response_text = None

    try:
        response_text = clean_json_response(await run_in_threadpool(chatbot.llm.invoke, formatted_prompt))
        parsed = json.loads(response_text)

        if missing_keys := set(CodeGenerationResponse.model_fields) - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            return CodeGenerationResponse(code="", explanation=msg, language="bash")

        return CodeGenerationResponse(**parsed)
    except json.JSONDecodeError as e:
        error_msg = "Invalid JSON response from LLM"
        raise get_server_error(error_msg, e, response_text) from e
    except Exception as e:
        error_msg = "Failed to generate or parse LLM response"
        raise get_server_error(error_msg, e, response_text) from e


@api_router.post("/explain-code", response_model=CodeExplanationResponse)
@limiter.limit(LIMITER_INTERVAL)
async def explain_code(request: Request, prompt_request: PromptRequest) -> CodeExplanationResponse:
    """Explain code step-by-step.

    The LLM automatically detects the language from the code syntax.
    """
    chatbot = request.app.state.chatbot
    formatted_prompt = sanitize_text(chatbot.prompt_code_explanation(prompt_request.prompt))
    response_text = None

    try:
        response_text = clean_json_response(await run_in_threadpool(chatbot.llm.invoke, formatted_prompt))
        parsed = json.loads(response_text)

        if missing_keys := set(CodeExplanationResponse.model_fields) - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            return CodeExplanationResponse(explanation=msg)

        return CodeExplanationResponse(**parsed)
    except json.JSONDecodeError as e:
        error_msg = "Invalid JSON response from LLM"
        raise get_server_error(error_msg, e, response_text) from e
    except Exception as e:
        error_msg = "Failed to generate or parse LLM response"
        raise get_server_error(error_msg, e, response_text) from e


@api_router.post("/search-exploits", response_model=ExploitSearchResponse)
@limiter.limit(LIMITER_INTERVAL)
async def search_exploits(request: Request, prompt: PromptRequest) -> ExploitSearchResponse:
    """Search for known exploits based on target description."""
    chatbot = request.app.state.chatbot
    formatted_prompt = sanitize_text(chatbot.prompt_exploit_search(prompt.prompt))
    response_text = None

    try:
        response_text = clean_json_response(await run_in_threadpool(chatbot.llm.invoke, formatted_prompt))
        parsed = json.loads(response_text)

        if missing_keys := set(ExploitSearchResponse.model_fields) - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            return ExploitSearchResponse(exploits=[], explanation=msg)

        return ExploitSearchResponse(**parsed)
    except json.JSONDecodeError as e:
        error_msg = "Invalid JSON response from LLM"
        raise get_server_error(error_msg, e, response_text) from e
    except Exception as e:
        error_msg = "Failed to generate or parse LLM response"
        raise get_server_error(error_msg, e, response_text) from e
