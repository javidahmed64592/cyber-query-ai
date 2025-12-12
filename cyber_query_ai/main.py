"""Main application module for the CyberQueryAI FastAPI server."""

from cyber_query_ai.server import CyberQueryAIServer


def run() -> None:
    """Serve the FastAPI application using uvicorn.

    :raise SystemExit: If configuration fails to load or SSL certificate files are missing
    """
    server = CyberQueryAIServer()
    server.run()
