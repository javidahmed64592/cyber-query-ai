"""CyberQueryAI."""

import os
from collections.abc import Callable
from pathlib import Path
from typing import cast

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from cyber_query_ai.api import get_api_router, get_limiter
from cyber_query_ai.chatbot import Chatbot
from cyber_query_ai.config import Config, load_config


def create_app(config: Config, api_router: APIRouter, limiter: Limiter) -> FastAPI:
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
    app.include_router(api_router)

    # Rate limiter setup
    app.state.limiter = limiter
    handler = cast(Callable[[Request, Exception], Response], _rate_limit_exceeded_handler)
    app.add_exception_handler(RateLimitExceeded, handler)
    app.add_middleware(SlowAPIMiddleware)

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


def run() -> None:
    """Run the FastAPI app using uvicorn."""
    config = load_config()
    api_router = get_api_router()
    limiter = get_limiter()
    app = create_app(config, api_router, limiter)
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
    )
