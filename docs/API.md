<!-- omit from toc -->
# API

This document summarizes the CyberQueryAI-specific API endpoints.

## Base Server Infrastructure

CyberQueryAI inherits from [python-template-server](https://github.com/javidahmed64592/python-template-server), which provides production-ready infrastructure including:

- **API Key Authentication**: All authenticated endpoints require the `X-API-KEY` header with a SHA-256 hashed token
- **Rate Limiting**: Configurable request throttling (default: 10 requests/minute per IP)
- **Security Headers**: Automatic HSTS, CSP, and X-Frame-Options enforcement
- **Request Logging**: Comprehensive logging of all requests/responses with client IP tracking
- **Health Checks**: Standard `/api/health` endpoint for availability monitoring
- **HTTPS Support**: Built-in SSL certificate generation and management

For detailed information about these features, authentication token generation, server middleware, and base configuration, see the [python-template-server README](https://github.com/javidahmed64592/python-template-server/blob/main/README.md).

<!-- omit from toc -->
## Table of Contents
- [Base Server Infrastructure](#base-server-infrastructure)
- [Endpoints](#endpoints)
  - [GET /api/config](#get-apiconfig)
  - [POST /api/model/chat](#post-apimodelchat)
  - [POST /api/code/generate](#post-apicodegenerate)
  - [POST /api/code/explain](#post-apicodeexplain)
  - [POST /api/exploit/search](#post-apiexploitsearch)
- [Request and Response Models (Pydantic)](#request-and-response-models-pydantic)
- [Error handling](#error-handling)
- [Sanitization and LLM handling](#sanitization-and-llm-handling)
- [Frontend integration notes](#frontend-integration-notes)


## Endpoints

All endpoints are mounted under the `/api` prefix and serve on `https://0.0.0.0:443` by default (configurable via `configuration/config.json`).
All LLM-driven endpoints expect JSON requests and return JSON responses following the `BaseResponse` schema (see [python-template-server models](https://github.com/javidahmed64592/python-template-server/blob/main/README.md) for details).
The backend sanitizes prompts and attempts to normalize LLM outputs to valid JSON before parsing.

### GET /api/config

- **Purpose**: Retrieve the current server configuration including model settings and version
- **Authentication**: Not required
- **Rate Limiting**: Not applied
- **Request**: None
- **Response model**: `GetApiConfigResponse` (extends `BaseResponse`)
    - code: number (200 for success)
    - message: string (config retrieval status)
    - timestamp: ISO 8601 string
    - model: `CyberQueryAIModelConfig` object
        - model: string (LLM model name, e.g., "mistral")
        - embedding_model: string (RAG embedding model, e.g., "bge-m3")
    - version: string (application version from package metadata)

Example response:
```json
{
    "code": 200,
    "message": "Successfully retrieved chatbot configuration.",
    "timestamp": "2025-12-13T12:00:00.000000Z",
    "model": {
        "model": "mistral",
        "embedding_model": "bge-m3"
    },
    "version": "1.0.4"
}
```

### POST /api/model/chat

- **Purpose**: Interactive conversational interface for general cybersecurity assistance with full conversation history support
- **Authentication**: Required
- **Rate Limiting**: Applied (10 requests/minute)
- **Request model**: `PostChatRequest`
    - message: string (user's message)
    - history: array of `ChatMessageModel` objects (conversation context)
        - role: "user" | "assistant"
        - content: string
- **Response model**: `PostChatResponse` (extends `BaseResponse`)
    - code: number (200 for success, 500 for errors)
    - message: string (operation status)
    - timestamp: ISO 8601 string
    - model_message: string (AI assistant's response with markdown support)

Notes:
- This is the **primary endpoint** for the AI Assistant interface (`/assistant`)
- Supports full conversation history, allowing for context-aware responses and follow-up questions
- The assistant can handle all types of requests: commands, scripts, explanations, exploit research, etc.
- Responses are formatted in markdown with code blocks when appropriate
- Both input prompt and output are sanitized using `sanitize_text()`
- LLM calls are executed via `run_in_threadpool` to prevent blocking the event loop

Example request:
```json
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
```

Example response:
```json
{
    "code": 200,
    "message": "Successfully generated chat response.",
    "timestamp": "2025-12-13T12:00:00.000000Z",
    "model_message": "To perform a stealth port scan with nmap, use the `-sS` flag:\n\n```bash\nnmap -sS target.com\n```\n\nThis performs a SYN scan which is less likely to be detected..."
}
```

### POST /api/code/generate

- **Purpose**: Generate cybersecurity code (CLI commands or scripts) from a user prompt. The LLM automatically infers whether to generate a command or script and which language to use based on the prompt
- **Authentication**: Required
- **Rate Limiting**: Applied (10 requests/minute)
- **Request model**: `PostPromptRequest`
    - prompt: string (task description)
- **Response model**: `PostCodeGenerationResponse` (extends `BaseResponse`)
    - code: number (200 for success, 500 for errors)
    - message: string (operation status or error description)
    - timestamp: ISO 8601 string
    - generated_code: string (single command or multi-line script, empty on error)
    - explanation: string (code explanation and context, empty on error)
    - language: string (e.g., "bash", "python", "powershell", empty on error)

Notes:
- The server formats the prompt using the chatbot prompt template, sanitizes it with `sanitize_text()`, and calls the LLM via `run_in_threadpool()`
- Raw LLM output is cleaned using `clean_json_response()` to fix common formatting issues before JSON parsing
- The LLM intelligently determines whether to generate a single command or a full script based on task complexity
- The language is automatically detected and returned (no need to specify upfront)
- If the LLM response is missing required fields, the endpoint returns HTTP 500 with an error message
- On JSON decode errors or exceptions, returns HTTP 500 with descriptive error in the `message` field

Example request (command):
```json
{
    "prompt": "enumerate open ports on a Linux host"
}
```

Example response (command):
```json
{
    "code": 200,
    "message": "Successfully generated code.",
    "timestamp": "2025-12-13T12:00:00.000000Z",
    "generated_code": "nmap -sC -sV target.example.com",
    "explanation": "This nmap command performs a service version detection scan with default scripts on the target host.",
    "language": "bash"
}
```

Example request (script):
```json
{
    "prompt": "download a file and compute its sha256 in python"
}
```

Example response (script):
```json
{
    "code": 200,
    "message": "Successfully generated code.",
    "timestamp": "2025-12-13T12:00:00.000000Z",
    "generated_code": "import requests\nimport hashlib\n\nurl = 'https://example.com/file.zip'\nresponse = requests.get(url)\n\nsha256_hash = hashlib.sha256(response.content).hexdigest()\nprint(f'SHA256: {sha256_hash}')",
    "explanation": "This Python script downloads a file using requests and computes its SHA256 hash by passing the downloaded content to hashlib.",
    "language": "python"
}
```

### POST /api/code/explain

- **Purpose**: Explain code (CLI commands or scripts) step-by-step. The LLM automatically detects the code type and provides an appropriate explanation
- **Authentication**: Required
- **Rate Limiting**: Applied (10 requests/minute)
- **Request model**: `PostPromptRequest`
    - prompt: string (the code to explain)
- **Response model**: `PostCodeExplanationResponse` (extends `BaseResponse`)
    - code: number (200 for success, 500 for errors)
    - message: string (operation status or error description)
    - timestamp: ISO 8601 string
    - explanation: string (detailed code explanation, empty on error)

Notes:
- The LLM automatically determines whether the code is a command or script and provides context-appropriate explanations
- No need to specify the language or code type upfront—the AI detects it from the code itself
- Explanations include parameter breakdowns for commands and line-by-line analysis for scripts
- Input is sanitized with `sanitize_text()` and LLM output is cleaned with `clean_json_response()`
- On JSON decode errors or exceptions, returns HTTP 500 with descriptive error in the `message` field

Example request (command):
```json
{
    "prompt": "tar -xzf archive.tar.gz"
}
```

Example response (command):
```json
{
    "code": 200,
    "message": "Successfully explained code.",
    "timestamp": "2025-12-13T12:00:00.000000Z",
    "explanation": "This tar command extracts a gzip-compressed archive:\n\n- `-x`: Extract files from an archive\n- `-z`: Filter the archive through gzip for decompression\n- `-f archive.tar.gz`: Specify the filename of the archive to extract\n\nThe command will extract all contents of archive.tar.gz to the current directory."
}
```

Example request (script):
```json
{
    "prompt": "#!/bin/bash\nwhile IFS= read -r line; do\n  echo \"$line\" | rev\ndone"
}
```

Example response (script):
```json
{
    "code": 200,
    "message": "Successfully explained code.",
    "timestamp": "2025-12-13T12:00:00.000000Z",
    "explanation": "This Bash script reads input line-by-line and reverses each line:\n\n- `while IFS= read -r line`: Reads each line from stdin, preserving whitespace\n- `echo \"$line\" | rev`: Outputs the line and pipes it to the rev command which reverses the string\n- `done`: Closes the while loop\n\nExample: Input 'hello' outputs 'olleh'."
}
```

### POST /api/exploit/search

- **Purpose**: Search for known exploits or vulnerabilities relevant to a target description
- **Authentication**: Required
- **Rate Limiting**: Applied (10 requests/minute)
- **Request model**: `PostPromptRequest`
    - prompt: string (target description)
- **Response model**: `PostExploitSearchResponse` (extends `BaseResponse`)
    - code: number (200 for success, 500 for errors)
    - message: string (operation status or error description)
    - timestamp: ISO 8601 string
    - exploits: array of `ExploitModel` objects (empty array on error)
        - title: string (exploit/CVE name)
        - link: string (URL to exploit details)
        - severity: string (e.g., "High", "Medium", "Low")
        - description: string (vulnerability details)
    - explanation: string (search context and findings summary, empty on error)

Notes:
- Input is sanitized with `sanitize_text()` and LLM output is cleaned with `clean_json_response()`
- On JSON decode errors or exceptions, returns HTTP 500 with descriptive error in the `message` field
- Empty `exploits` array if no relevant vulnerabilities are found

Example request:
```json
{
    "prompt": "service running an old version of OpenSSH"
}
```

Example response:
```json
{
    "code": 200,
    "message": "Successfully searched for exploits.",
    "timestamp": "2025-12-13T12:00:00.000000Z",
    "exploits": [
        {
            "title": "OpenSSH Remote Code Execution",
            "link": "https://example.com/cve-xxxx",
            "severity": "High",
            "description": "Details about the vulnerability and affected versions"
        }
    ],
    "explanation": "Found CVEs and public exploit code references relevant to the provided description."
}
```

## Request and Response Models (Pydantic)

All response models extend `BaseResponse` from python-template-server, which provides:
- `code`: number (HTTP-style response code)
- `message`: string (human-readable status message)
- `timestamp`: string (ISO 8601 formatted timestamp)

The primary Pydantic models are defined in `cyber_query_ai/models.py`:

**Request Models:**
- `PostChatRequest`: { message: str, history: list[ChatMessageModel] }
- `PostPromptRequest`: { prompt: str }
- `ChatMessageModel`: { role: RoleType ("user" | "assistant"), content: str }

**Response Models (all extend BaseResponse):**
- `GetApiConfigResponse`: { model: CyberQueryAIModelConfig, version: str }
- `PostChatResponse`: { model_message: str }
- `PostCodeGenerationResponse`: { generated_code: str, explanation: str, language: str }
- `PostCodeExplanationResponse`: { explanation: str }
- `PostExploitSearchResponse`: { exploits: list[ExploitModel], explanation: str }

**Configuration Models:**
- `CyberQueryAIModelConfig`: { model: str, embedding_model: str }
- `CyberQueryAIConfig` (extends `TemplateServerConfig`): { model: CyberQueryAIModelConfig, server: ServerConfig, security: SecurityConfig, rate_limit: RateLimitConfig, certificate: CertificateConfig, json_response: JSONResponseConfig }

**Other Models:**
- `ExploitModel`: { title: str, link: str, severity: str, description: str }
- `RoleType`: Enum with values "user" and "assistant"

**Note**: `HealthResponse` is provided by python-template-server and includes `status: str` in addition to BaseResponse fields.

## Error handling

**Successful Responses**: All successful responses return HTTP 200 with `code: 200` in the JSON body.

**Error Responses**: Errors are returned with appropriate HTTP status codes and structured JSON responses:

- **Authentication Failures** (401): Missing or invalid `X-API-KEY` header
  ```json
  {
      "detail": "Unauthorized: Invalid or missing API key"
  }
  ```

- **Rate Limiting** (429): Too many requests
  ```json
  {
      "detail": "Rate limit exceeded: 10 per 1 minute"
  }
  ```

- **LLM Processing Errors** (HTTP 200 with `code: 500`): Invalid LLM output, JSON parsing failures, or missing required fields
  ```json
  {
      "code": 500,
      "message": "Invalid JSON response from LLM: <raw text>",
      "timestamp": "2025-12-13T12:00:00.000000Z",
      "generated_code": "",
      "explanation": "",
      "language": ""
  }
  ```

- **Server Errors** (500): Unexpected exceptions
  ```json
  {
      "code": 500,
      "message": "An unexpected error occurred during code generation.",
      "timestamp": "2025-12-13T12:00:00.000000Z",
      "generated_code": "",
      "explanation": "",
      "language": ""
  }
  ```

**Error Handling Strategy**:
- LLM endpoints return valid response models even on errors (with `code: 500` and empty data fields)
- This allows the frontend to handle errors gracefully without parsing exceptions
- Detailed error messages are always provided in the `message` field
- Authentication and rate limiting errors use standard HTTP error responses from TemplateServer

## Sanitization and LLM handling

**Input Sanitization**:
- All user prompts are sanitized using `sanitize_text()` from `helpers.py` before being sent to the LLM
- `sanitize_text()` uses `bleach.clean()` to strip HTML tags and potentially dangerous content
- This prevents injection attacks and ensures clean LLM inputs

**LLM Response Processing**:
1. **Threadpool Execution**: All LLM calls are executed via `run_in_threadpool(self.chatbot.llm.invoke, formatted_prompt)` to prevent blocking the event loop
2. **JSON Cleaning**: Raw LLM output is passed through `clean_json_response()` which:
   - Strips markdown code fences (```json, etc.)
   - Converts single quotes to double quotes for JSON compatibility
   - Removes trailing commas that break JSON parsing
   - Handles common LLM formatting quirks
3. **Parsing**: Cleaned response is parsed with `json.loads()`
4. **Validation**: Parsed JSON is validated against Pydantic models
5. **Field Checking**: Endpoints verify all required fields are present in the LLM response

**RAG System**:
- The `RAGSystem` class in `rag.py` injects relevant tool documentation into prompts
- Uses `bge-m3` embedding model for semantic similarity search
- Tool metadata from `rag_data/tools.json` is embedded and retrieved based on prompt content
- Top-3 similar documents are injected into the prompt with escaped braces for LangChain compatibility

## Frontend integration notes

**API Client** (`src/lib/api.ts`):
- Centralized API communication using axios
- Request interceptor automatically adds `X-API-KEY` header from localStorage
- Response interceptor handles authentication errors (redirects to login on 401)
- 30-second timeout for LLM endpoints
- Functions: `sendChatMessage()`, `generateCode()`, `explainCode()`, `searchExploits()`, `getConfig()`, `loginWithApiKey()`

**Authentication Flow** (`src/contexts/AuthContext.tsx`):
- `AuthProvider` wraps the entire application in `layout.tsx`
- API key stored in localStorage as 'api_key'
- `useAuth()` hook provides `login()`, `logout()`, and `isAuthenticated` state
- Automatic redirect to `/login/` for unauthenticated users
- Login page (`src/app/login/page.tsx`) validates API key via `/api/login` endpoint

**Type Safety** (`src/lib/types.ts`):
- TypeScript interfaces mirror backend Pydantic models
- All interfaces extend `BaseResponse`: { code: number, message: string, timestamp: string }
- Must be kept in sync with `cyber_query_ai/models.py`

**Development Proxy** (`next.config.ts`):
- Reads `configuration/config.json` at build time
- Proxies `/api/*` requests to backend in development mode

**Production Deployment**:
- Next.js static export (`output: "export"`)
- Frontend served from `static/` directory by FastAPI
- API calls use same-origin `/api` paths (no proxy needed)

**Error Handling** (`src/components/ErrorNotification.tsx`):
- Portal-based toast notifications using `createPortal(component, document.body)`
- `useErrorNotification()` hook for displaying errors
- Auto-dismiss after 5 seconds
- z-index 9999 for top-level rendering above all UI elements

**Configuration**:
- `configuration/config.json` is the single source of truth for:
  - Server host/port
  - Model configuration (LLM and embedding models)
  - Rate limiting settings
  - Security headers
  - SSL certificate configuration
- Backend reads it via `CyberQueryAIConfig.load_from_file()`
- Frontend development proxy reads it via `next.config.ts`
- Available to frontend at runtime via `/api/config` endpoint
