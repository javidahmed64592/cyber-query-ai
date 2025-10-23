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
    CommandGenerationResponse,
    ConfigResponse,
    ExplanationResponse,
    ExploitSearchResponse,
    HealthResponse,
    PromptRequest,
    PromptWithLanguageRequest,
    ScriptGenerationResponse,
)

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
        response_text = await run_in_threadpool(chatbot.llm, formatted_prompt)
        return ChatResponse(message=sanitize_text(response_text))
    except Exception as e:
        msg = "Failed to generate chat response"
        raise get_server_error(msg, e, response_text) from e


@api_router.post("/generate-command", response_model=CommandGenerationResponse)
@limiter.limit(LIMITER_INTERVAL)
async def generate_command(request: Request, prompt: PromptRequest) -> CommandGenerationResponse:
    """Generate cybersecurity commands based on user prompt."""
    chatbot = request.app.state.chatbot
    formatted_prompt = sanitize_text(chatbot.prompt_command_generation(prompt.prompt))
    response_text = None

    try:
        response_text = clean_json_response(await run_in_threadpool(chatbot.llm, formatted_prompt))
        parsed = json.loads(response_text)

        if missing_keys := set(CommandGenerationResponse.model_fields) - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            return CommandGenerationResponse(commands=[], explanation=msg)

        return CommandGenerationResponse(**parsed)
    except json.JSONDecodeError as e:
        msg = "Invalid JSON response from LLM"
        raise get_server_error(msg, e, response_text) from e
    except Exception as e:
        msg = "Failed to generate or parse LLM response"
        raise get_server_error(msg, e, response_text) from e


@api_router.post("/generate-script", response_model=ScriptGenerationResponse)
@limiter.limit(LIMITER_INTERVAL)
async def generate_script(request: Request, prompt: PromptWithLanguageRequest) -> ScriptGenerationResponse:
    """Generate a script in the specified language based on user prompt."""
    chatbot = request.app.state.chatbot
    formatted_prompt = sanitize_text(chatbot.prompt_script_generation(prompt.language, prompt.prompt))
    response_text = None

    try:
        response_text = clean_json_response(await run_in_threadpool(chatbot.llm, formatted_prompt))
        parsed = json.loads(response_text)

        if missing_keys := set(ScriptGenerationResponse.model_fields) - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            return ScriptGenerationResponse(script="", explanation=msg)

        return ScriptGenerationResponse(**parsed)
    except json.JSONDecodeError as e:
        msg = "Invalid JSON response from LLM"
        raise get_server_error(msg, e, response_text) from e
    except Exception as e:
        msg = "Failed to generate or parse LLM response"
        raise get_server_error(msg, e, response_text) from e


@api_router.post("/explain-command", response_model=ExplanationResponse)
@limiter.limit(LIMITER_INTERVAL)
async def explain_command(request: Request, prompt: PromptRequest) -> ExplanationResponse:
    """Explain a CLI command step-by-step."""
    chatbot = request.app.state.chatbot
    formatted_prompt = sanitize_text(chatbot.prompt_command_explanation(prompt.prompt))
    response_text = None

    try:
        response_text = clean_json_response(await run_in_threadpool(chatbot.llm, formatted_prompt))
        parsed = json.loads(response_text)

        if missing_keys := set(ExplanationResponse.model_fields) - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            return ExplanationResponse(explanation=msg)

        return ExplanationResponse(**parsed)
    except json.JSONDecodeError as e:
        msg = "Invalid JSON response from LLM"
        raise get_server_error(msg, e, response_text) from e
    except Exception as e:
        msg = "Failed to generate or parse LLM response"
        raise get_server_error(msg, e, response_text) from e


@api_router.post("/explain-script", response_model=ExplanationResponse)
@limiter.limit(LIMITER_INTERVAL)
async def explain_script(request: Request, prompt: PromptWithLanguageRequest) -> ExplanationResponse:
    """Explain a script in the specified language step-by-step."""
    chatbot = request.app.state.chatbot
    formatted_prompt = sanitize_text(chatbot.prompt_script_explanation(prompt.language, prompt.prompt))
    response_text = None

    try:
        response_text = clean_json_response(await run_in_threadpool(chatbot.llm, formatted_prompt))
        parsed = json.loads(response_text)

        if missing_keys := set(ExplanationResponse.model_fields) - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            return ExplanationResponse(explanation=msg)

        return ExplanationResponse(**parsed)
    except json.JSONDecodeError as e:
        msg = "Invalid JSON response from LLM"
        raise get_server_error(msg, e, response_text) from e
    except Exception as e:
        msg = "Failed to generate or parse LLM response"
        raise get_server_error(msg, e, response_text) from e


@api_router.post("/search-exploits", response_model=ExploitSearchResponse)
@limiter.limit(LIMITER_INTERVAL)
async def search_exploits(request: Request, prompt: PromptRequest) -> ExploitSearchResponse:
    """Search for known exploits based on target description."""
    chatbot = request.app.state.chatbot
    formatted_prompt = sanitize_text(chatbot.prompt_exploit_search(prompt.prompt))
    response_text = None

    try:
        response_text = clean_json_response(await run_in_threadpool(chatbot.llm, formatted_prompt))
        parsed = json.loads(response_text)

        if missing_keys := set(ExploitSearchResponse.model_fields) - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            return ExploitSearchResponse(exploits=[], explanation=msg)

        return ExploitSearchResponse(**parsed)
    except json.JSONDecodeError as e:
        msg = "Invalid JSON response from LLM"
        raise get_server_error(msg, e, response_text) from e
    except Exception as e:
        msg = "Failed to generate or parse LLM response"
        raise get_server_error(msg, e, response_text) from e
