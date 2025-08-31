"""Helper methods for the CyberQueryAI application."""

import os
import re
from pathlib import Path

import bleach
from fastapi.responses import FileResponse


def get_static_dir() -> Path:
    """Get the static directory path."""
    return Path(os.environ.get("CYBER_QUERY_AI_ROOT_DIR", ".") or ".") / "static"


def get_static_files(full_path: str, static_dir: Path) -> FileResponse | None:
    """Get the static files for a given full path."""
    # Skip API routes - they should be handled by the API router
    if full_path.startswith("api/"):
        return None

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

    return None


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


def sanitize_text(prompt: str) -> str:
    """Sanitize user input and LLM output for security."""
    prompt = re.sub(r"<script[^>]*>.*?</script>", "", prompt, flags=re.IGNORECASE | re.DOTALL)
    return str(bleach.clean(prompt, tags=[], strip=True)).strip()
