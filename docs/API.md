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
  - [GET /api/config](#get-apiconfig)
  - [POST /api/chat](#post-apichat)
  - [POST /api/generate-code](#post-apigenerate-code)
  - [POST /api/explain-code](#post-apiexplain-code)
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

### GET /api/config

- Purpose: Retrieve the current server configuration.
- Request: none
- Response model: `ConfigResponse`
    - model: string (LLM model name, e.g., "mistral")
    - embedding_model: string (RAG embedding model, e.g., "bge-m3")
    - host: string (server host, e.g., "localhost")
    - port: number (server port, e.g., 8000)

Example response:
{
    "model": "mistral",
    "embedding_model": "bge-m3",
    "host": "localhost",
    "port": 8000
}

### POST /api/chat

- Purpose: Interactive conversational interface for general cybersecurity assistance with full conversation history support.
- Request model: `ChatRequest`
    - message: string (user's message)
    - history: array of `ChatMessage` objects (conversation context)
        - role: "user" | "assistant"
        - content: string
- Response model: `ChatResponse`
    - message: string (AI assistant's response with markdown support)

Notes:
- This is the **primary endpoint** for the AI Assistant interface (home page `/`)
- Supports full conversation history, allowing for context-aware responses and follow-up questions
- The assistant can handle all types of requests: commands, scripts, explanations, exploit research, etc.
- Responses are formatted in markdown with code blocks when appropriate
- Both input and output are sanitized using `sanitize_text()`

Example request:
{
    "message": "How do I perform a stealth port scan?",
    "history": [
        {
            "role": "user",
            "content": "What is nmap used for?"
        },
        {
            "role": "assistant",
            "content": "Nmap is a network scanning tool..."
        }
    ]
}

Example response:
{
    "message": "To perform a stealth port scan with nmap, use the `-sS` flag:\n\n```bash\nnmap -sS target.com\n```\n\nThis performs a SYN scan which is less likely to be detected..."
}

### POST /api/generate-code

- Purpose: Generate cybersecurity code (CLI commands or scripts) from a user prompt. The LLM automatically infers whether to generate a command or script and which language to use based on the prompt.
- Request model: `PromptRequest`
    - prompt: string
- Response model: `CodeGenerationResponse`
    - code: string (single command or multi-line script)
    - explanation: string
    - language: string (e.g., "bash", "python", "powershell", etc.)

Notes:
- The server formats the prompt using the chatbot prompt template, sanitizes it, calls the LLM and then tries to clean the LLM response into JSON (`clean_json_response`).
- The LLM intelligently determines whether to generate a single command or a full script based on the complexity of the request.
- The language is automatically detected and returned (no need to specify upfront).
- If required keys are missing from the parsed JSON, the response will still be returned with an explanation describing the issue.

Example request (command):
{
    "prompt": "enumerate open ports on a Linux host"
}

Example response (command):
{
    "code": "nmap -sC -sV target.example.com",
    "explanation": "This nmap command performs a service version detection scan with default scripts on the target host.",
    "language": "bash"
}

Example request (script):
{
    "prompt": "download a file and compute its sha256 in python"
}

Example response (script):
{
    "code": "import requests\nimport hashlib\n\nurl = 'https://example.com/file.zip'\nresponse = requests.get(url)\n\nsha256_hash = hashlib.sha256(response.content).hexdigest()\nprint(f'SHA256: {sha256_hash}')",
    "explanation": "This Python script downloads a file using requests and computes its SHA256 hash by passing the downloaded content to hashlib.",
    "language": "python"
}

### POST /api/explain-code

- Purpose: Explain code (CLI commands or scripts) step-by-step. The LLM automatically detects the code type and provides an appropriate explanation.
- Request model: `PromptRequest`
    - prompt: string (the code to explain)
- Response model: `CodeExplanationResponse`
    - explanation: string

Notes:
- The LLM automatically determines whether the code is a command or script and provides context-appropriate explanations.
- No need to specify the language or code type upfront—the AI detects it from the code itself.
- Explanations include parameter breakdowns for commands and line-by-line analysis for scripts.

Example request (command):
{
    "prompt": "tar -xzf archive.tar.gz"
}

Example response (command):
{
    "explanation": "This tar command extracts a gzip-compressed archive:\n\n- `-x`: Extract files from an archive\n- `-z`: Filter the archive through gzip for decompression\n- `-f archive.tar.gz`: Specify the filename of the archive to extract\n\nThe command will extract all contents of archive.tar.gz to the current directory."
}

Example request (script):
{
    "prompt": "#!/bin/bash\nwhile IFS= read -r line; do\n  echo \"$line\" | rev\ndone"
}

Example response (script):
{
    "explanation": "This Bash script reads input line-by-line and reverses each line:\n\n- `while IFS= read -r line`: Reads each line from stdin, preserving whitespace\n- `echo \"$line\" | rev`: Outputs the line and pipes it to the rev command which reverses the string\n- `done`: Closes the while loop\n\nExample: Input 'hello' outputs 'olleh'."
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
- ChatMessage: { role: Literal["user", "assistant"], content: str }
- ChatRequest: { message: str, history: list[ChatMessage] }
- ChatResponse: { message: str }
- PromptRequest: { prompt: str }
- HealthResponse: { status: str, timestamp: str }
- ConfigResponse: { model: str, embedding_model: str, host: str, port: int }
- CodeGenerationResponse: { code: str, explanation: str, language: str }
- CodeExplanationResponse: { explanation: str }
- Exploit: { title: str, link: str, severity: str, description: str }
- ExploitSearchResponse: { exploits: list[Exploit], explanation: str }

## Error handling

- Server errors are returned with HTTP 500 and a JSON `detail` object with keys `error`, `details` (exception string), and `raw` (raw LLM text if available).
- If the LLM returns invalid JSON, a 500 is raised with detail indicating a JSON decode failure.
- If the LLM response is missing required fields, the endpoint returns a valid response model with an explanatory message in the `explanation` field (or empty string for `code`, or empty list for `exploits`).

## Sanitization and LLM handling

- Prompts are sanitized before being sent to the LLM (`sanitize_text`).
- The raw LLM output is passed through `clean_json_response` to coerce/clean JSON-like text before parsing.
- LLM calls are executed off the main event loop with `run_in_threadpool(chatbot.llm, prompt)`.

## Frontend integration notes

- The Next.js frontend uses `src/lib/api.ts` and expects the backend API under `/api` (same-origin in production, proxied in development).
- In development mode, `next.config.ts` reads `config.json` at build time to configure the proxy URL for API requests.
- Client helper functions: `sendChatMessage`, `generateCode`, `explainCode`, `searchExploits`, `getConfig` map directly to the endpoints above and expect the response shapes listed.
- The `config.json` file is the single source of truth for host and port configuration, used by both the backend server and the Next.js development proxy.
