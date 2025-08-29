"""Cyber Query AI."""

import json

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

from cyber_query_ai.chatbot import Chatbot
from cyber_query_ai.config import load_config
from cyber_query_ai.models import CommandGenerationResponse, PromptRequest

config = load_config()
chatbot = Chatbot(model=config.model)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router = APIRouter(prefix="/api")


@api_router.post("/generate-command", response_model=CommandGenerationResponse)
async def generate_command(request: PromptRequest) -> CommandGenerationResponse:
    """Generate cybersecurity commands based on user prompt."""
    formatted_prompt = chatbot.prompt_command_generation(task=request.prompt)
    response_text = None
    try:
        response_text = await run_in_threadpool(chatbot.llm, formatted_prompt)
        parsed = json.loads(response_text)
        if missing_keys := {"commands", "explanation"} - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            return CommandGenerationResponse(commands=[], explanation=msg)

        return CommandGenerationResponse(**parsed)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to generate or parse LLM response",
                "details": str(e),
                "raw": str(response_text) if response_text else "No response",
            },
        ) from e


app.include_router(api_router)


def run() -> None:
    """Run the FastAPI app using uvicorn."""
    uvicorn.run(
        "cyber_query_ai.main:app",
        host=config.host,
        port=config.port,
        reload=True,
    )
