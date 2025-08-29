"""Cyber Query AI."""

import json

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

from cyber_query_ai.chatbot import Chatbot
from cyber_query_ai.config import Config, load_config
from cyber_query_ai.models import CommandGenerationResponse, PromptRequest

api_router = APIRouter(prefix="/api")


def create_app(config: Config) -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.chatbot = Chatbot(model=config.model)
    return app


@api_router.post("/generate-command", response_model=CommandGenerationResponse)
async def generate_command(request: PromptRequest, app_request: Request) -> CommandGenerationResponse:
    """Generate cybersecurity commands based on user prompt."""
    chatbot = app_request.app.state.chatbot
    formatted_prompt = chatbot.prompt_command_generation(task=request.prompt)
    response_text = None

    try:
        response_text = await run_in_threadpool(chatbot.llm, formatted_prompt)
        parsed = json.loads(response_text)
        if not (missing_keys := {"commands", "explanation"} - parsed.keys()):
            return CommandGenerationResponse(**parsed)

        msg = f"Missing required keys in LLM response: {missing_keys}"
        return CommandGenerationResponse(commands=[], explanation=msg)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to generate or parse LLM response",
                "details": str(e),
                "raw": str(response_text) if response_text else "No response",
            },
        ) from e


def run() -> None:
    """Run the FastAPI app using uvicorn."""
    config = load_config()
    app = create_app(config)
    app.include_router(api_router)
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
    )
