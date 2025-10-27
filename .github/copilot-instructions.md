# CyberQueryAI Development Guide

## Project Overview

CyberQueryAI is an AI-powered cybersecurity assistant that converts natural language into security commands, scripts, and insights using local Ollama LLMs. The system combines FastAPI (Python 3.12+) with Next.js 16 (TypeScript/React 19) to provide ethical hacking tools for authorized penetration testing.

## Architecture Patterns

### Backend: FastAPI + LangChain + Ollama

- **Single chatbot instance**: Created once in `main.create_app()` and stored on `app.state.chatbot` for all routes to share
- **Configuration on app.state**: Config loaded from `config.json` and stored on `app.state.config` for app-wide access
- **Async LLM calls**: Always wrap `chatbot.llm()` with `run_in_threadpool()` to prevent blocking the event loop
- **JSON-only LLM contract**: All prompts enforce strict JSON responses; use `clean_json_response()` before `json.loads()` to handle LLM formatting quirks (code blocks, single quotes, trailing commas)
- **RAG-enhanced prompts**: The `RAGSystem` injects relevant tool documentation into prompts using vector similarity search (embeddings via `bge-m3`)

### Frontend: Next.js App Router + Static Export

- **Dual deployment modes**: Dev uses Next.js rewrites to proxy `/api` requests; production serves static build from `static/` with same-origin API calls
- **Single source of truth**: `config.json` is read by `next.config.ts` at build time to configure the dev proxy URL
- **Error mapping in api.ts**: All backend calls flow through `src/lib/api.ts` which standardizes error handling and timeouts (30s for LLM responses)
- **Type safety**: Keep `src/lib/types.ts` interfaces synchronized with backend Pydantic models in `cyber_query_ai/models.py`

## Critical Development Workflows

### Building & Running

```bash
# Backend only
uv sync --extra dev
cyber-query-ai  # Runs on localhost:8000 by default

# Frontend dev (proxies to backend)
cd cyber-query-ai-frontend
npm install
npm run dev  # http://localhost:3000

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

### Input/Output Sanitization

- **Backend**: All user prompts and LLM responses pass through `sanitize_text()` (uses `bleach` to strip HTML/scripts)
- **Frontend**: User inputs sanitized via `sanitizeInput()`, LLM outputs via `sanitizeOutput()` (DOMPurify) before rendering
- **Command safety**: Client-side `isCommandSafe()` flags risky patterns (`rm -rf`, `shutdown`, etc.) with warnings

### Rate Limiting

- **5 requests/minute per IP** on all LLM endpoints using SlowAPI
- Disable in tests with `limiter.enabled = False` (see `tests/test_api.py`)

## Code Conventions

### Python (Ruff + mypy enforced)

- **120 char lines**, strict type hints, comprehensive docstrings (D203/D213 style)
- **Error responses**: Use `get_server_error()` helper to return structured errors with `error`, `details`, and `raw` (LLM text) fields
- **Pydantic everywhere**: Models in `models.py` for request/response validation
- **Mock threadpool in tests**: Use `@patch("cyber_query_ai.api.run_in_threadpool")` fixture to avoid actual LLM calls

### TypeScript (ESLint + Prettier enforced)

- **No async clipboard without try/catch**: Always wrap `navigator.clipboard.writeText()` (see `CommandBox.tsx`)
- **DOMPurify for LLM content**: Never render LLM text without sanitization
- **Axios error handling**: Check `axios.isAxiosError()` → `error.response` → `error.request` → fallback (see `api.ts` pattern)

## Key Files & Their Roles

### Backend

- `api.py`: Route definitions including `/api/config` and `/api/chat` endpoints; all LLM calls wrapped in `run_in_threadpool()` + `clean_json_response()` + model validation
- `chatbot.py`: Prompt templates with strict JSON formatting rules; RAG context injection; includes `prompt_chat()` for conversational interface
- `rag.py`: Vector store creation from `rag_data/*.txt` with metadata from `tools.json`
- `helpers.py`: `clean_json_response()` repairs LLM output (strips markdown, fixes quotes, removes trailing commas)
- `models.py`: All Pydantic models including `ConfigResponse`, `ChatMessage`, `ChatRequest`, and `ChatResponse` used throughout the application
- `config.py`: Loads `config.json` and returns `ConfigResponse` model from `models.py`

### Frontend

- `src/lib/api.ts`: Single source for all backend communication including `getConfig()` and `sendChatMessage()`; 30s timeout, error normalization
- `src/lib/types.ts`: TypeScript interfaces synchronized with backend Pydantic models, including `ConfigResponse`, `ChatMessage`, `ChatRequest`, and `ChatResponse`
- `src/lib/sanitization.ts`: DOMPurify wrapper + command safety checker
- `src/components/`: Presentational components including `ChatWindow.tsx` and `ChatMessage.tsx` for conversational interface; keep business logic in `api.ts`
- `next.config.ts`: Reads `config.json` at build time to configure dev proxy; uses `ConfigResponse` type

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
3. Package installer (`release/` with `.sh` and `.bat` scripts)
4. Verify installer creates virtualenv, copies static files, generates service scripts

## Deployment & Installation

### Pre-built Release Structure

The build workflow creates a release package containing:

- Python wheel (`cyber_query_ai-*.whl`)
- Static frontend files in `static/` directory
- `install_cyber_query_ai.sh` (Linux/macOS)
- `install_cyber_query_ai.bat` (Windows)
- `readme.txt` (comprehensive installation guide)

### Installer Script Behavior

**Linux/macOS (`install_cyber_query_ai.sh`)**:

1. Creates `.venv` using `uv venv`
2. Installs wheel with `uv pip install`, then deletes wheel
3. Extracts `config.json`, `README.md`, `SECURITY.md`, `LICENSE` from site-packages to root
4. Generates `cyber-query-ai` bash executable that sets `CYBER_QUERY_AI_ROOT_DIR` and launches app
5. Creates systemd service file in `service/cyber_query_ai.service` with auto-restart on failure
6. Generates `service/start_service.sh` and `service/stop_service.sh` for service management
7. Creates `uninstall_cyber_query_ai.sh` that removes entire installation directory
8. Self-deletes installer files after completion

**Windows (`install_cyber_query_ai.bat`)**:

1. Creates `.venv` using `uv venv`
2. Installs wheel with `uv pip install`, then deletes wheel
3. Extracts config/docs from `Lib\site-packages` to root
4. Generates `cyber-query-ai.bat` launcher that:
   - Sets `CYBER_QUERY_AI_ROOT_DIR` environment variable
   - Starts Ollama server in background (`start /b ollama serve`)
   - Runs application
   - Kills Ollama process on exit (`taskkill /f /im ollama.exe`)
5. Self-deletes installer files after completion
6. **Note**: Windows installer automatically manages Ollama lifecycle; Linux/macOS requires manual Ollama setup

### Static File Serving Pattern

The application serves the Next.js static export using this priority:

1. API routes (`/api/*`) handled by FastAPI router
2. Exact file matches in `static/` directory
3. Directory with `index.html` (e.g., `/about` → `static/about/index.html`)
4. Fallback to `static/index.html` for SPA routing
5. 404 if no match

See `helpers.py:get_static_files()` for implementation.

### Service Management (Linux/macOS)

The generated systemd service includes:

- **User context**: Runs as installing user (not root)
- **Auto-restart**: Restarts on failure with 5s delay
- **Rate limiting**: Max 5 restarts per 60s
- **Logging**: Appends to `cyber_query_ai.log`
- **Security**: `ProtectSystem=full` with read-write access only to install directory

Service location: `/etc/systemd/system/cyber_query_ai.service`

### Post-Installation Configuration

Users must:

1. Pull required Ollama models: `ollama pull mistral && ollama pull bge-m3`
2. Edit `config.json` to customize model, host, port
3. Ensure Ollama is running (Linux/macOS) or trust Windows launcher to start it

## Configuration

### `config.json` (required at runtime)

```json
{
  "model": "mistral", // Ollama LLM model
  "embedding_model": "bge-m3", // For RAG embeddings
  "host": "localhost",
  "port": 8000
}
```

**Note:** `config.json` is the single source of truth for all configuration:

- Backend server reads it to configure host/port and model settings
- `next.config.ts` reads it at build time to configure the development proxy
- Available via `/api/config` endpoint returning `ConfigResponse` model

### Environment variables

- `CYBER_QUERY_AI_ROOT_DIR`: Points to application root

## Common Pitfalls

1. **Forgetting `run_in_threadpool()`**: LLM calls block the event loop → use async wrapper
2. **Not cleaning LLM JSON**: Always use `clean_json_response()` before parsing
3. **Frontend/backend type drift**: Update both `types.ts` and `models.py` together (especially `ConfigResponse`)
4. **Missing sanitization**: All user input and LLM output must be sanitized
5. **Config model location**: `ConfigResponse` is defined in `models.py` (not `config.py`) and imported by `config.load_config()`
6. **Breaking version checks**: Update all 3 files when bumping versions
7. **Ollama not running**: Application requires local Ollama server at runtime
8. **Directory context in terminal commands**: Check the current working directory before using `cd` commands; if already in the target directory, omit the `cd` command to avoid errors

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
