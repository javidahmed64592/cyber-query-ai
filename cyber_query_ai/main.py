"""CyberQueryAI."""

import json
import os
import re
from pathlib import Path

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from cyber_query_ai.chatbot import Chatbot
from cyber_query_ai.config import Config, load_config
from cyber_query_ai.models import CommandGenerationResponse, PromptRequest

api_router = APIRouter(prefix="/api")


def clean_json_response(response_text: str) -> str:
    """Clean common JSON formatting issues from LLM responses."""
    # Remove trailing commas in arrays and objects
    response_text = re.sub(r",(\s*[}\]])", r"\1", response_text)

    # Remove any markdown code blocks if present
    response_text = re.sub(r"```json\s*", "", response_text)
    response_text = re.sub(r"```\s*$", "", response_text)

    # Fix common structural issues where explanation is inside commands array
    # Pattern: ["command", "explanation": "text"] -> ["command"], "explanation": "text"
    response_text = re.sub(
        r'(\["[^"]*"\s*),\s*"(explanation?)":\s*"([^"]*)"(\s*\])',
        r'\1], "\2": "\3"',
        response_text,
        flags=re.IGNORECASE,
    )

    # Strip whitespace
    return response_text.strip()


def create_app(config: Config) -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[f"http://{config.host}:{config.port}"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
    app.state.chatbot = Chatbot(model=config.model)

    # Serve static files if they exist
    static_dir = Path(os.environ.get("CYBER_QUERY_AI_ROOT_DIR", ".") or ".") / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

        # Serve index.html for SPA routing (must be defined after API routes)
        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str) -> FileResponse:
            """Serve the SPA for all non-API routes."""
            # Skip API routes - they should be handled by the API router
            if full_path.startswith("api/"):
                raise HTTPException(status_code=404, detail="API endpoint not found")

            # Serve specific static files
            file_path = static_dir / full_path
            if file_path.is_file():
                return FileResponse(file_path)

            # Check if it's a directory with index.html
            if file_path.is_dir():
                index_path = file_path / "index.html"
                if index_path.is_file():
                    return FileResponse(index_path)

            # Fallback to index.html for SPA routing
            index_path = static_dir / "index.html"
            if index_path.exists():
                return FileResponse(index_path)

            raise HTTPException(status_code=404, detail="File not found")

    return app


@api_router.post("/generate-command", response_model=CommandGenerationResponse)
async def generate_command(request: PromptRequest, app_request: Request) -> CommandGenerationResponse:
    """Generate cybersecurity commands based on user prompt."""
    chatbot = app_request.app.state.chatbot
    formatted_prompt = chatbot.prompt_command_generation(task=request.prompt)
    response_text = None

    try:
        response_text = await run_in_threadpool(chatbot.llm, formatted_prompt)
        cleaned_response = clean_json_response(response_text)

        parsed = json.loads(cleaned_response)
        if not (missing_keys := {"commands", "explanation"} - parsed.keys()):
            return CommandGenerationResponse(**parsed)

        msg = f"Missing required keys in LLM response: {missing_keys}"
        return CommandGenerationResponse(commands=[], explanation=msg)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Invalid JSON response from LLM",
                "details": f"JSON parsing failed: {e!s}",
                "raw": str(response_text) if response_text else "No response",
            },
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to generate or parse LLM response",
                "details": f"{e!s}",
                "raw": str(response_text) if response_text else "No response",
            },
        ) from e


def run() -> None:
    """Run the FastAPI app using uvicorn."""
    config = load_config()
    app = create_app(config)
    # Include API router before any catch-all routes
    app.include_router(api_router)
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
    )
