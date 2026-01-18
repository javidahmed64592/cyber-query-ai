"""Helper methods for the CyberQueryAI application."""

import json
import re
from pathlib import Path

import bleach
from python_template_server.constants import ROOT_DIR


def get_rag_tools_path() -> Path:
    """Get the rag tools file path."""
    return Path(ROOT_DIR) / "rag_data" / "tools.json"


def clean_json_response(response_text: str) -> str:
    """Clean common JSON formatting issues from LLM responses."""
    # Remove any markdown code blocks wrapping the entire response
    response_text = re.sub(r"```json\s*", "", response_text)
    response_text = re.sub(r"```\s*$", "", response_text)

    # First, try to parse as-is in case it's already valid JSON
    try:
        json.loads(response_text.strip())
        return response_text.strip()
    except json.JSONDecodeError:
        pass

    # If parsing failed, try to fix common issues

    # Step 1: Handle markdown code blocks within string values
    # Replace triple backticks with escaped versions to avoid JSON parsing issues
    response_text = response_text.replace("```python", "```\\npython")
    response_text = response_text.replace("```", "")

    # Step 2: Fix unescaped quotes within string values - common contractions
    response_text = re.sub(r'client\\"s', "client's", response_text)
    response_text = re.sub(r'(\w)\\"(\w)', r"\1'\2", response_text)  # Fix contractions like don\"t -> don't
    response_text = re.sub(r'\\"(\w)', r"'\1", response_text)  # Fix quote at start of word like \"Hello -> 'Hello

    # Step 3: Convert Python dict syntax to JSON syntax by replacing single quotes with double quotes
    # First, temporarily replace escaped quotes to avoid confusion
    response_text = response_text.replace("\\'", "__ESCAPED_SINGLE_QUOTE__")
    response_text = response_text.replace('\\"', "__ESCAPED_DOUBLE_QUOTE__")

    # Replace single quotes used as string delimiters with double quotes
    # This regex matches single quotes that are used as string delimiters (not inside strings)
    response_text = re.sub(r"'([^']*)'", r'"\1"', response_text)

    # Restore escaped quotes
    response_text = response_text.replace("__ESCAPED_SINGLE_QUOTE__", "\\'")
    response_text = response_text.replace("__ESCAPED_DOUBLE_QUOTE__", '\\"')

    # Step 4: Remove trailing commas in arrays and objects
    response_text = re.sub(r",(\s*[}\]])", r"\1", response_text)

    # Step 5: Fix common structural issues where explanation is inside commands array
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
