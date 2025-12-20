<!-- omit from toc -->
# Architecture

This document summarizes the code architecture and technology stack for the CyberQueryAI application.

<!-- omit from toc -->
## Table of Contents
- [Technology Stack](#technology-stack)
- [High-Level Architecture](#high-level-architecture)
- [Backend Structure: `cyber_query_ai`](#backend-structure-cyber_query_ai)
- [Frontend Structure: `cyber-query-ai-frontend`](#frontend-structure-cyber-query-ai-frontend)
- [Operational notes](#operational-notes)


## Technology Stack
- Backend: Python 3.13+, python-template-server (FastAPI base), Uvicorn, Pydantic, LangChain, langchain-ollama (OllamaLLM), Bleach (sanitization)
- Frontend: Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS, Axios for API calls, DOMPurify (client-side sanitization)
- Authentication: X-API-KEY header with SHA-256 hashed tokens (provided by python-template-server)
- Rate Limiting: SlowAPI with configurable storage (in-memory/Redis/Memcached, default: in-memory)
- Observability: Prometheus metrics, request logging, health checks (provided by python-template-server)
- Dev / tooling: pytest, Ruff, mypy, Jest, ESLint, Prettier, TypeScript, Ollama for local LLM hosting

## High-Level Architecture

- The backend inherits from `TemplateServer` (from python-template-server package), which provides production-ready infrastructure including authentication, rate limiting, security headers, request logging, and Prometheus metrics.
- `CyberQueryAIServer` extends `TemplateServer` and implements domain-specific endpoints for LLM-driven cybersecurity tasks.
- The server creates a `Chatbot` instance (wrapping an Ollama LLM with RAG support) during initialization and stores it as `self.chatbot`.
- Static frontend files are served from the `static/` directory with SPA fallback routing.
- The frontend is a Next.js application that calls backend endpoints via `src/lib/api.ts`. In production it expects same-origin `/api` paths; in development Next.js proxies requests to the HTTPS backend.
- Configuration is centralized in `configuration/cyber_query_ai_config.json` and extends `TemplateServerConfig` with application-specific model settings.

## Backend Structure: `cyber_query_ai`

- `server.py`
    - `CyberQueryAIServer` class extends `TemplateServer` from python-template-server
    - Overrides `validate_config()` to load `CyberQueryAIConfig` (extends `TemplateServerConfig`)
    - Overrides `setup_routes()` to register application-specific endpoints:
        - `GET /api/config` - Unauthenticated route returning model config and version
        - `POST /api/model/chat` - **Primary endpoint** for AI Assistant with conversation history
        - `POST /api/code/generate` - Generate commands or scripts (language inferred by LLM)
        - `POST /api/code/explain` - Explain commands or scripts (type detected by LLM)
        - `POST /api/exploit/search` - Search for exploits and vulnerabilities
        - `GET /{full_path:path}` - SPA fallback serving static files
    - Creates and stores `Chatbot` instance with RAG support during initialization
    - Mounts static files from `static/` directory if present
    - Rate limiting (10 requests/minute) applied to authenticated endpoints via TemplateServer middleware
    - All LLM endpoints use `run_in_threadpool()` to prevent blocking the event loop

- `main.py`
    - Simple entry point that creates `CyberQueryAIServer()` instance and calls `server.run()`
    - Server reads configuration from `configuration/cyber_query_ai_config.json` via `CyberQueryAIConfig.load_from_file()`
    - Uvicorn configured for HTTPS with SSL certificates from `certs/` directory

- `chatbot.py`
    - `Chatbot` class wraps `OllamaLLM` and provides prompt templates (via LangChain `PromptTemplate`) for each use case: chat assistance, code generation, code explanation, exploit search
    - Initializes `RAGSystem` for context-enhanced prompts using tool documentation from `rag_data/tools.json`
    - Enforces strict JSON-only response contract in prompt templates with detailed formatting rules
    - `prompt_chat()` supports conversational interactions with full history context for the AI Assistant interface
    - `prompt_code_generation()`, `prompt_code_explanation()`, and `prompt_exploit_search()` methods format prompts for specialized endpoints
    - All prompt templates include RAG-injected context with relevant tool documentation

- `rag.py`
    - `RAGSystem` class provides semantic search over cybersecurity tool documentation
    - Uses `bge-m3` Ollama embedding model for vector similarity search
    - Loads tool metadata from `rag_data/tools.json` and corresponding `.txt` files
    - `generate_rag_content()` retrieves top-3 similar documents based on prompt content
    - Injects retrieved context into prompts with escaped braces for LangChain compatibility

- `helpers.py`
    - Sanitization: `sanitize_text()` uses `bleach.clean()` to strip HTML/scripts from user input and LLM output
    - JSON cleaning: `clean_json_response()` repairs common LLM formatting issues (code fences, single quotes, trailing commas)
    - Static file serving: `get_static_dir()` locates `static/` directory, `get_static_files()` handles SPA fallback logic
    - Filepath helpers: `get_rag_tools_path()` for retrieving the RAG directory

- `models.py`
    - Pydantic models for all request/response types
    - All response models extend `BaseResponse` from python-template-server (code, message, timestamp)
    - `CyberQueryAIConfig` extends `TemplateServerConfig` and adds `model: CyberQueryAIModelConfig`
    - Request models: `PostChatRequest`, `PostPromptRequest`, `ChatMessageModel`
    - Response models: `GetApiConfigResponse`, `PostChatResponse`, `PostCodeGenerationResponse`, `PostCodeExplanationResponse`, `PostExploitSearchResponse`
    - Other models: `ExploitModel`, `RoleType` enum, `CyberQueryAIModelConfig`

## Frontend Structure: `cyber-query-ai-frontend`

- `src/app/`
  - Next.js App Router pages and layouts
  - `layout.tsx` - Root layout wrapping application in `AuthProvider`
  - `page.tsx` - Home page with AI Assistant conversational interface
  - `login/page.tsx` - API key authentication page
  - `code-generation/page.tsx` - Code generation interface
  - `code-explanation/page.tsx` - Code explanation interface
  - `exploit-search/page.tsx` - Exploit search interface
  - `about/page.tsx` - Application information and documentation
  - `404/page.tsx` - Custom 404 error page

- `src/contexts/`
    - `AuthContext.tsx` - Global authentication state management
        - Provides `login()`, `logout()`, `isAuthenticated` state
        - Stores API key in localStorage as 'api_key'
        - Automatic redirect to `/login/` for unauthenticated users
        - Uses `useRef` to prevent redirect loops

- `src/components/`
    - `ChatWindow.tsx` - Main conversational interface for AI Assistant with message history
    - `ChatMessage.tsx` - Individual message rendering with markdown support and code block syntax highlighting
    - `ErrorNotification.tsx` - Portal-based toast notifications using `createPortal(component, document.body)` for z-index management
    - `ScriptBox.tsx`, `ExplanationBox.tsx` - Code output and loading states for specialized pages
    - `ExploitList.tsx` - Exploit search results with severity badges
    - `Navigation.tsx` - App navigation with health indicator and logout button
    - `HealthIndicator.tsx` - Real-time server status display
    - `Footer.tsx` - Application footer with version and model information

- `src/lib/api.ts`
  - Centralized API client using axios
  - Request interceptor automatically adds `X-API-KEY` header from `getApiKey()`
  - Response interceptor handles 401 errors (redirects to login)
  - 30-second timeout for LLM endpoints
  - Functions: `loginWithApiKey()`, `sendChatMessage()`, `generateCode()`, `explainCode()`, `searchExploits()`, `getConfig()`, `getHealth()`
  - Error handling: `extractErrorMessage()`, `isSuccessResponse()` for unified error processing
  - `useHealthStatus()` hook for polling server health status

- `src/lib/auth.ts`
  - localStorage management for API key persistence
  - Functions: `saveApiKey()`, `getApiKey()`, `removeApiKey()`, `isAuthenticated()`

- `src/lib/types.ts`
  - TypeScript interfaces mirroring backend Pydantic models
  - `BaseResponse`: { code: number, message: string, timestamp: string }
  - All response types extend `BaseResponse`
  - Request types: `ChatRequest`, `PromptRequest`, `ChatMessage`
  - Response types: `ApiConfigResponse`, `ChatResponse`, `CodeGenerationResponse`, `CodeExplanationResponse`, `ExploitSearchResponse`, `HealthResponse`
  - Must be kept in sync with `cyber_query_ai/models.py`

- `src/lib/sanitization.ts`
  - Client-side input/output sanitization
  - `sanitizeInput()` - Basic text cleaning for user inputs
  - `sanitizeOutput()` - DOMPurify wrapper for LLM-provided content
  - `isCommandSafe()` - Command safety checker (flags dangerous patterns)

- `next.config.ts`
  - Reads `configuration/cyber_query_ai_config.json` at build time
  - Development proxy: rewrites `/api/*` to HTTPS backend
  - Custom `https.Agent` with `rejectUnauthorized: false` for self-signed certificates
  - Sets `NODE_TLS_REJECT_UNAUTHORIZED=0` environment variable
  - Static export configuration (`output: "export"`)
  - Type-safe config parsing using `CyberQueryAIConfig` interface

## Operational notes

**Authentication**:
- API key authentication provided by python-template-server using X-API-KEY header
- API tokens are SHA-256 hashed and stored in `.env` file (backend)
- Generate new tokens using `uv run generate-new-token` command
- Frontend stores API key in localStorage and includes it in all authenticated requests

**Rate Limiting**:
- 10 requests/minute per IP address on authenticated endpoints
- Configured via `configuration/cyber_query_ai_config.json` `rate_limit` section
- Can be disabled by setting `enabled: false` in config
- Supports multiple storage backends: in-memory (default), Redis, Memcached
- Rate limit errors return HTTP 429 with descriptive message

**LLM Integration**:
- Uses local Ollama via `langchain-ollama.OllamaLLM`
- Default model: `mistral` (configurable in `configuration/cyber_query_ai_config.json`)
- Embedding model: `bge-m3` for RAG semantic search
- All LLM calls executed via `run_in_threadpool()` to prevent event loop blocking
- Responses cleaned with `clean_json_response()` before JSON parsing

**Security**:
- Input sanitization: `sanitize_text()` using `bleach` for all user prompts
- Output sanitization: Client-side DOMPurify for LLM-generated content
- Security headers: HSTS, CSP, X-Frame-Options automatically applied by TemplateServer
- HTTPS only: Self-signed certificates generated via `uv run generate-certificate`
- Command safety: Client-side `isCommandSafe()` flags dangerous patterns

**Error Handling**:
- Authentication errors: HTTP 401 with redirect to `/login/`
- Rate limiting: HTTP 429 with retry-after information
- LLM errors: HTTP 200 with `code: 500` in JSON body (includes error message in `message` field)
- Server errors: HTTP 500 with descriptive error message
- All LLM endpoint errors return valid response models with empty data fields

**Monitoring & Observability**:
- Prometheus metrics at `/api/metrics` (authentication, rate limiting, HTTP stats)
- Health check at `/api/health` (returns server status)
- Request logging with client IP tracking (configured in `TemplateServer`)
- Custom metrics for LLM performance and error rates

**Static File Serving**:
- Frontend built as Next.js static export to `static/` directory
- Served by FastAPI with SPA fallback routing
- Priority: exact file match → directory/index.html → fallback to index.html → 404
- Implemented in `helpers.get_static_files()` and `server.serve_spa()`

**Configuration**:
- Single source of truth: `configuration/cyber_query_ai_config.json`
- Extends `TemplateServerConfig` with `model: CyberQueryAIModelConfig`
- Loaded via `CyberQueryAIConfig.load_from_file()` method
- Available at runtime via `/api/config` endpoint (unauthenticated)
- Used by backend server, Next.js development proxy, and frontend runtime
