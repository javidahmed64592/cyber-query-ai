"""Main application module for the CyberQueryAI FastAPI server."""

from cyber_query_ai.server import CyberQueryAIServer


def run() -> None:
    """Serve the FastAPI application using uvicorn."""
    server = CyberQueryAIServer()
    server.run()
