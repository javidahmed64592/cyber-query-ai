<!-- omit from toc -->
# API

This document summarizes the backend API provided by the CyberQueryAI FastAPI application. All endpoints are mounted under the `/api` prefix.

Rate limiting: 5 requests per minute (per client IP) on endpoints that call the LLM.

All LLM-driven endpoints expect JSON requests and return JSON responses.
The backend sanitizes prompts and attempts to normalize LLM outputs to valid JSON before parsing.

<!-- omit from toc -->
## Table of Contents
- [Endpoints](#endpoints)
  - [GET /api/health](#get-apihealth)
  - [POST /api/generate-command](#post-apigenerate-command)
  - [POST /api/generate-script](#post-apigenerate-script)
  - [POST /api/explain-command](#post-apiexplain-command)
  - [POST /api/explain-script](#post-apiexplain-script)
  - [POST /api/search-exploits](#post-apisearch-exploits)
- [Request and Response Models (Pydantic)](#request-and-response-models-pydantic)
- [Error handling](#error-handling)
- [Sanitization and LLM handling](#sanitization-and-llm-handling)
- [Frontend integration notes](#frontend-integration-notes)


## Endpoints

### GET /api/health

- Purpose: Simple health check of the server.
- Request: none
- Response model: `HealthResponse`
    - status: string
    - timestamp: ISO 8601 string

Example response:
{
    "status": "healthy",
    "timestamp": "2025-09-02T12:00:00Z"
}

### POST /api/generate-command

- Purpose: Generate cybersecurity CLI commands plus an explanation from a user prompt.
- Request model: `PromptRequest`
    - prompt: string
- Response model: `CommandGenerationResponse`
    - commands: list[string]
    - explanation: string

Notes:
- The server formats the prompt using the chatbot prompt template, sanitizes it, calls the LLM and then tries to clean the LLM response into JSON (`clean_json_response`).
- If required keys are missing from the parsed JSON, the response will still be returned as the Pydantic model with empty commands and an explanation describing the missing keys.

Example request:
{
    "prompt": "enumerate open ports on a Linux host"
}

Example response:
{
    "commands": ["nmap -sC -sV target.example.com", "ss -tuln"],
    "explanation": "Use nmap for network scanning and ss to list listening sockets locally."
}

### POST /api/generate-script

- Purpose: Generate a script in a specified language from a prompt.
- Request model: `PromptWithLanguageRequest`
    - prompt: string
    - language: string
- Response model: `ScriptGenerationResponse`
    - script: string
    - explanation: string

Example request:
{
    "prompt": "download a file and compute its sha256",
    "language": "python"
}

Example response:
{
    "script": "import requests, hashlib\n...",
    "explanation": "This script downloads a file and computes its sha256 by streaming bytes to the hasher."
}

### POST /api/explain-command

- Purpose: Explain a CLI command step-by-step.
- Request model: `PromptRequest`
    - prompt: string
- Response model: `ExplanationResponse`
    - explanation: string

Example request:
{
    "prompt": "tar -xzf archive.tar.gz"
}

Example response:
{
    "explanation": "tar -xzf extracts a gzip-compressed tar archive; -x extract, -z filter through gzip, -f specify file."
}

### POST /api/explain-script

- Purpose: Explain a script in a given language step-by-step.
- Request model: `PromptWithLanguageRequest`
    - prompt: string
    - language: string
- Response model: `ExplanationResponse`
    - explanation: string

Example request:
{
    "prompt": "for each line print reversed line",
    "language": "bash"
}

Example response:
{
    "explanation": "This script reads stdin line-by-line and reverses each line using parameter expansion..."
}

### POST /api/search-exploits

- Purpose: Search for known exploits or vulnerabilities relevant to a target description.
- Request model: `PromptRequest`
    - prompt: string
- Response model: `ExploitSearchResponse`
    - exploits: list of `Exploit` objects
        - title: string
        - link: string
        - severity: string
        - description: string
    - explanation: string

Example request:
{
    "prompt": "service running an old version of OpenSSH"
}

Example response:
{
    "exploits": [
        {
            "title": "OpenSSH Remote Code Execution",
            "link": "https://example.com/cve-xxxx",
            "severity": "high",
            "description": "Details about the vulnerability and affected versions"
        }
    ],
    "explanation": "Found CVEs and public exploit code references relevant to the provided description."
}

## Request and Response Models (Pydantic)

The primary Pydantic models are defined in `cyber_query_ai/models.py`:
- PromptRequest: { prompt: str }
- PromptWithLanguageRequest: { prompt: str, language: str }
- HealthResponse: { status: str, timestamp: str }
- CommandGenerationResponse: { commands: list[str], explanation: str }
- ScriptGenerationResponse: { script: str, explanation: str }
- ExplanationResponse: { explanation: str }
- Exploit: { title: str, link: str, severity: str, description: str }
- ExploitSearchResponse: { exploits: list[Exploit], explanation: str }

## Error handling

- Server errors are returned with HTTP 500 and a JSON `detail` object with keys `error`, `details` (exception string), and `raw` (raw LLM text if available).
- If the LLM returns invalid JSON, a 500 is raised with detail indicating a JSON decode failure.
- If the LLM response is missing required fields, the endpoint returns a valid response model with an explanatory message in the `explanation` field (or empty list for `commands`/`exploits`).

## Sanitization and LLM handling

- Prompts are sanitized before being sent to the LLM (`sanitize_text`).
- The raw LLM output is passed through `clean_json_response` to coerce/clean JSON-like text before parsing.
- LLM calls are executed off the main event loop with `run_in_threadpool(chatbot.llm, prompt)`.

## Frontend integration notes

- The Next.js frontend uses `src/lib/api.ts` and expects the backend API under `/api` (same-origin in production, proxied in development).
- Client helper functions: `generateCommand`, `generateScript`, `explainCommand`, `explainScript`, `searchExploits` map directly to the endpoints above and expect the response shapes listed.
