# CyberQueryAI Development Guide

## Project Overview

CyberQueryAI is an AI-powered cybersecurity assistant that converts natural language into security commands, scripts, and insights using local Ollama LLMs. The system extends python-template-server (FastAPI-based with built-in authentication, rate limiting, and observability) and combines it with Next.js 16 (TypeScript/React 19) to provide ethical hacking tools for authorized penetration testing.

## Architecture Patterns

### Backend: TemplateServer + LangChain + Ollama

- **TemplateServer inheritance**: `CyberQueryAIServer` extends `TemplateServer` from python-template-server, inheriting authentication (X-API-KEY), rate limiting (10/min), security headers, request logging, and Prometheus metrics
- **Single chatbot instance**: Created during `CyberQueryAIServer.__init__()` and stored as `self.chatbot` for all routes to access
- **Configuration**: Config loaded from `configuration/cyber_query_ai_config.json` using `CyberQueryAIConfig.load_from_file()` which extends `TemplateServerConfig`
- **Async LLM calls**: Always wrap `self.chatbot.llm.invoke()` with `run_in_threadpool()` to prevent blocking the event loop
- **JSON-only LLM contract**: All prompts enforce strict JSON responses; use `clean_json_response()` before `json.loads()` to handle LLM formatting quirks (code blocks, single quotes, trailing commas)
- **RAG-enhanced prompts**: The `RAGSystem` injects relevant tool documentation into prompts using vector similarity search (embeddings via `bge-m3`)
- **HTTPS-only**: Server runs on port 443 with SSL certificates from `certs/` directory (auto-generated or via `uv run generate-certificate`)

### Frontend: Next.js App Router + Static Export + Authentication

- **Dual deployment modes**: Dev uses Next.js HTTPS proxy to backend; production serves static build from `static/` with same-origin API calls
- **Single source of truth**: `configuration/cyber_query_ai_config.json` is read by `next.config.ts` at build time to configure the dev proxy URL (HTTPS with self-signed cert support)
- **Authentication**: X-API-KEY header authentication managed via `AuthContext` with localStorage persistence; automatic redirect to `/login/` for unauthenticated users
- **API client with interceptors**: `src/lib/api.ts` adds X-API-KEY header to all requests and handles 401 redirects
- **Error notifications**: Portal-based toast notifications using `createPortal(component, document.body)` for proper z-index stacking
- **Type safety**: Keep `src/lib/types.ts` interfaces synchronized with backend Pydantic models in `cyber_query_ai/models.py` (all response types extend `BaseResponse`)
- **Executing commands**: Always `cd` into the fully resolved `cyber-query-ai-frontend` directory before running npm commands to avoid context issues

## Critical Development Workflows

### Building & Running

```bash
# Backend prerequisites
ollama serve  # Ensure Ollama is running
ollama pull mistral && ollama pull bge-m3  # Pull required models
uv run generate-new-token  # Generate API authentication token
uv run generate-certificate  # Generate SSL certificate (optional, auto-generated)

# Backend only
uv sync --extra dev
cyber-query-ai  # Runs on https://localhost:443 by default

# Frontend dev (proxies to HTTPS backend)
cd cyber-query-ai-frontend
npm install
npm run dev  # http://localhost:3000 (proxies /api to https://localhost:443)

# Production build
npm run build:static  # Outputs to ../static/
```

### Testing

```bash
# Backend (pytest with coverage)
uv run -m pytest --cov-report html

# Frontend (Jest)
cd cyber-query-ai-frontend
npm run test

# All checks
npm run quality  # type-check + lint + format
```

### Version consistency check

The CI enforces version alignment across `pyproject.toml`, `uv.lock`, and `cyber-query-ai-frontend/package.json`. Update all three when releasing.

## Security & Sanitization Requirements

### Authentication

- **X-API-KEY header**: All authenticated endpoints require this header with a SHA-256 hashed token
- **Token generation**: Use `uv run generate-new-token` to create tokens (hash stored in `.env` file)
- **Frontend storage**: API key stored in localStorage via `src/lib/auth.ts` (saveApiKey, getApiKey, removeApiKey, isAuthenticated)
- **Route protection**: `AuthContext` wraps app and redirects unauthenticated users to `/login/` using `useRef` to prevent redirect loops
- **Unauthenticated endpoints**: `/api/health`, `/api/config`, and static file serving do not require authentication

### Input/Output Sanitization

- **Backend**: All user prompts and LLM responses pass through `sanitize_text()` (uses `bleach` to strip HTML/scripts)
- **Frontend**: User inputs sanitized via `sanitizeInput()`, LLM outputs via `sanitizeOutput()` (DOMPurify) before rendering
- **Command safety**: Client-side `isCommandSafe()` flags risky patterns (`rm -rf`, `shutdown`, etc.) with warnings

### Rate Limiting

- **10 requests/minute per IP** on authenticated LLM endpoints (configurable in `configuration/cyber_query_ai_config.json`)
- Provided by python-template-server using SlowAPI with in-memory storage (supports Redis/Memcached)
- Disable in tests with `limiter.enabled = False`

## Code Conventions

### Python (Ruff + mypy enforced)

- **120 char lines**, strict type hints, comprehensive docstrings (D203/D213 style)
- **BaseResponse structure**: All response models extend `BaseResponse` from python-template-server (code: int, message: str, timestamp: str)
- **Pydantic everywhere**: Models in `models.py` for request/response validation; `CyberQueryAIConfig` extends `TemplateServerConfig`
- **Mock threadpool in tests**: Use `@patch("cyber_query_ai.server.run_in_threadpool")` fixture to avoid actual LLM calls
- **Error handling**: LLM endpoints return valid response models even on errors (with `code: 500` and empty data fields)

### TypeScript (ESLint + Prettier enforced)

- **BaseResponse everywhere**: All response interfaces extend `BaseResponse: { code: number, message: string, timestamp: string }`
- **DOMPurify for LLM content**: Never render LLM text without sanitization
- **Axios interceptors**: Request interceptor adds X-API-KEY header from `getApiKey()`; response interceptor handles 401 redirects
- **Portal for notifications**: Use `createPortal(component, document.body)` for toast notifications to avoid z-index issues
- **Auth context**: Use `useAuth()` hook for login/logout functionality and `isAuthenticated` state

## Key Files & Their Roles

### Backend

- `server.py`: `CyberQueryAIServer` class extending `TemplateServer`; overrides `validate_config()` and `setup_routes()` to register domain-specific endpoints; creates `Chatbot` instance during `__init__()`; handles static file serving with SPA fallback
- `main.py`: Entry point that creates `CyberQueryAIServer()` and calls `server.run()`
- `chatbot.py`: Prompt templates with strict JSON formatting rules; RAG context injection; includes `prompt_chat()` for conversational interface, `prompt_code_generation()`, `prompt_code_explanation()`, and `prompt_exploit_search()`
- `rag.py`: Vector store creation from `rag_data/*.txt` with metadata from `rag_data/tools.json`; semantic search using `bge-m3` embeddings
- `helpers.py`: `clean_json_response()` repairs LLM output (strips markdown, fixes quotes, removes trailing commas); `sanitize_text()` uses bleach; `get_static_files()` handles SPA routing for static files; `get_rag_tools_path()` and `get_static_dir()` return paths
- `models.py`: All Pydantic models including `CyberQueryAIConfig`, `CyberQueryAIModelConfig`, `PostChatRequest`, `PostChatResponse`, `PostCodeGenerationResponse`, `PostCodeExplanationResponse`, `PostExploitSearchResponse`, `GetApiConfigResponse`, `PostLoginResponse`; all response models extend `BaseResponse`

### Frontend

- `src/lib/api.ts`: Single source for all backend communication; axios instance with request interceptor (adds X-API-KEY) and response interceptor (handles 401); includes `loginWithApiKey()`, `sendChatMessage()`, `generateCode()`, `explainCode()`, `searchExploits()`, `getConfig()`, `getHealth()`; 30s timeout, error normalization
- `src/lib/auth.ts`: localStorage management for API key (saveApiKey, getApiKey, removeApiKey, isAuthenticated)
- `src/contexts/AuthContext.tsx`: Global authentication state with `login()`, `logout()`, redirect logic using `useRef` to prevent loops; wraps app in `layout.tsx`
- `src/lib/types.ts`: TypeScript interfaces synchronized with backend Pydantic models; all extend `BaseResponse: { code: number, message: string, timestamp: string }`
- `src/lib/sanitization.ts`: DOMPurify wrapper + command safety checker
- `src/components/ErrorNotification.tsx`: Portal-based toast notifications using `createPortal(component, document.body)` with z-index 9999; `useErrorNotification()` hook
- `src/components/`: Presentational components including `ChatWindow.tsx`, `ChatMessage.tsx`, `Navigation.tsx` (with logout), `Footer.tsx`, `HealthIndicator.tsx`; keep business logic in `api.ts`
- `src/app/login/page.tsx`: API key authentication page with form validation
- `next.config.ts`: Reads `configuration/cyber_query_ai_config.json` at build time; HTTPS proxy with custom agent (`rejectUnauthorized: false`) for self-signed certs; `NODE_TLS_REJECT_UNAUTHORIZED=0`

## RAG System Details

The RAG system enhances prompts with relevant tool documentation:

1. **Indexing**: `rag_data/tools.json` maps tool metadata to `rag_data/*.txt` files
2. **Embedding**: Uses `bge-m3` Ollama model for semantic search
3. **Retrieval**: Top-3 similar docs injected into prompt with escaped braces (`{{`, `}}`) for LangChain compatibility
4. **Context format**: Includes tool name, category, tags, use cases, and source file

## CI/CD Pipeline

### CI Workflow (`.github/workflows/ci.yml`)

- **Ruff**: Linting/formatting
- **mypy**: Type checking
- **pytest**: Backend tests with coverage
- **Frontend**: type-check + lint + format + jest
- **version-check**: Ensures `pyproject.toml`, `uv.lock`, `package.json` versions match

### Build Workflow (`.github/workflows/build.yml`)

1. Build Python wheel (`uv build`)
2. Build Next.js static export (`npm run build`)
3. Package installer (`release/` with `.sh` script)
4. Verify installer creates virtualenv, copies static files, and generates launchers

## Deployment & Installation

### Pre-built Release Structure

The build workflow creates a release package containing:

- Python wheel (`cyber_query_ai-*.whl`)
- Static frontend files in `static/` directory
- `install_cyber_query_ai.sh` (Linux/macOS)
- `readme.txt` (comprehensive installation guide)

### Installer Script Behavior

**Linux/macOS (`install_cyber_query_ai.sh`)**:

1. Creates `.venv` using `uv venv`
2. Installs wheel with `uv pip install`, then deletes wheel
3. Extracts required files from site-packages to root
4. Generates `cyber-query-ai` bash executable that launches app
5. Creates `uninstall_cyber_query_ai.sh` that removes entire installation directory
6. Self-deletes installer files after completion

### Static File Serving Pattern

The application serves the Next.js static export using this priority:

1. API routes (`/api/*`) handled by FastAPI router
2. Exact file matches in `static/` directory
3. Directory with `index.html` (e.g., `/about` → `static/about/index.html`)
4. Fallback to `static/index.html` for SPA routing
5. 404 if no match

See `helpers.py:get_static_files()` for implementation.

### Post-Installation Configuration

Users must:

1. Pull required Ollama models: `ollama pull mistral && ollama pull bge-m3`
2. Generate API authentication token: `uv run generate-new-token` (save the displayed token!)
3. Generate SSL certificate: `uv run generate-certificate` (or auto-generated on first run)
4. Edit `configuration/cyber_query_ai_config.json` to customize server settings (host, port, models, rate limits)
5. Ensure Ollama is running: `ollama serve`
6. Access application at `https://localhost:443` and login with API token

## Configuration

### `configuration/cyber_query_ai_config.json` (required at runtime)

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 443
  },
  "security": {
    "hsts_max_age": 31536000,
    "content_security_policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
  },
  "rate_limit": {
    "enabled": true,
    "rate_limit": "10/minute",
    "storage_uri": ""
  },
  "certificate": {
    "directory": "certs",
    "ssl_keyfile": "key.pem",
    "ssl_certfile": "cert.pem",
    "days_valid": 365
  },
  "json_response": {
    "ensure_ascii": false,
    "allow_nan": false,
    "indent": null,
    "media_type": "application/json; charset=utf-8"
  },
  "model": {
    "model": "mistral",
    "embedding_model": "bge-m3"
  }
}
```

**Note:** `configuration/cyber_query_ai_config.json` is the single source of truth for all configuration:

- Backend server reads it via `CyberQueryAIConfig.load_from_file()` (extends `TemplateServerConfig`)
- `next.config.ts` reads it at build time to configure the development proxy
- Available via `/api/config` endpoint returning `GetApiConfigResponse` with model config and version
- The `model` section is specific to CyberQueryAI; other sections are inherited from TemplateServerConfig

## Common Pitfalls

1. **Forgetting `run_in_threadpool()`**: LLM calls block the event loop → use async wrapper
2. **Not cleaning LLM JSON**: Always use `clean_json_response()` before parsing
3. **Frontend/backend type drift**: Update both `types.ts` and `models.py` together; ensure all response types extend `BaseResponse`
4. **Missing sanitization**: All user input and LLM output must be sanitized
5. **Wrong config path**: Configuration is in `configuration/cyber_query_ai_config.json` (not `config.json`)
6. **Missing authentication**: Most endpoints require X-API-KEY header; generate token with `uv run generate-new-token`
7. **Breaking version checks**: Update all 3 files when bumping versions (`pyproject.toml`, `uv.lock`, `package.json`)
8. **Ollama not running**: Application requires local Ollama server with `mistral` and `bge-m3` models at runtime
9. **HTTPS certificate warnings**: Self-signed certificates cause browser warnings in dev; this is expected
10. **Redirect loops**: Use `useRef` in AuthContext to track redirect state and prevent infinite loops
11. **Z-index stacking**: Use `createPortal(component, document.body)` for notifications to avoid stacking context issues
12. **Directory context in terminal commands**: Check the current working directory before using `cd` commands; if already in the target directory, omit the `cd` command to avoid errors

## Terminal Command Best Practices

When using `run_in_terminal` tool:

1. **Check terminal context**: Review the `<context>` section for the current working directory (`Cwd:`) before running commands
2. **Avoid redundant `cd` commands**: If the terminal is already in the correct directory, run the command directly without `cd`
3. **Use full paths for cross-directory commands**: When running commands from the project root that need to operate on frontend files, either:
   - Use full paths: `npm --prefix cyber-query-ai-frontend install`
   - Change directory once, then run multiple commands
4. **Pattern for sequential commands in same directory**:

   ```bash
   # Bad: Changes directory twice
   cd cyber-query-ai-frontend && npm install
   cd cyber-query-ai-frontend && npm run test

   # Good: Check context first
   # If Cwd is already cyber-query-ai-frontend:
   npm install
   npm run test
   ```

5. **Windows-specific**: On Windows (PowerShell), commands like `cd cyber-query-ai-frontend && npm install` work, but checking context is still important

## Ethical Guidelines

This project is exclusively for **authorized penetration testing** and **educational purposes**. All features assume:

- User has explicit written permission for target systems
- Activities occur in controlled lab environments
- Tools are used in compliance with applicable laws

When adding new features, maintain this ethical focus and include appropriate warnings/disclaimers.
