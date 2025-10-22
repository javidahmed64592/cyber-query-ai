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
- Backend: Python 3.12+, FastAPI, Uvicorn, Pydantic, LangChain, langchain-ollama (OllamaLLM), SlowAPI (rate limiting), Bleach (sanitization)
- Frontend: Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, Zustand (state), Axios for API calls
- Dev / tooling: pytest, Jest, ESLint, Prettier, TypeScript, Ollama for local LLM hosting

## High-Level Architecture

- The backend is a FastAPI app that exposes a small set of LLM-driven endpoints under `/api` and serves a static frontend (if present) from the `static/` directory.
- The backend creates a `Chatbot` instance (wrapping an Ollama LLM) and stores it on `app.state.chatbot` so API routes can access it.
- The frontend is a Next.js application that calls the backend endpoints via `src/lib/api.ts`. In production it expects same-origin `/api` paths; in development Next rewrites/proxies to the backend.

## Backend Structure: `cyber_query_ai`

- `main.py`
    - Application factory `create_app(config, api_router, limiter)`.
    - Registers `Chatbot` instance on `app.state.chatbot`.
    - Stores configuration on `app.state.config` for app-wide access.
    - Configures CORS, rate limiter (SlowAPI), static file mounting, and an SPA fallback route.
    - `run()` reads `config.json` (via `config.load_config`) and runs Uvicorn.

- `api.py`
    - Defines API router (`/api`) and endpoints:
        - `GET /api/health`
        - `GET /api/config`
        - `POST /api/generate-command`
        - `POST /api/generate-script`
        - `POST /api/explain-command`
        - `POST /api/explain-script`
        - `POST /api/search-exploits`
    - Rate-limited (5/min) on LLM endpoints using `slowapi.Limiter`.
    - Calls `chatbot` to format prompts, sanitizes them, runs LLM calls off the event loop using `run_in_threadpool`, cleans LLM JSON-like text (`clean_json_response`) and validates/parses responses into Pydantic models.

- `chatbot.py`
    - `Chatbot` class wraps an `OllamaLLM` LLM and provides prompt templates (via LangChain `PromptTemplate`) for each use case: command generation, script generation, explanations, exploit search.
    - Enforces a strict JSON-only response contract in the prompt templates (the LLM is instructed to reply in valid JSON with clearly documented rules).

- `helpers.py`
    - Sanitization helpers: `sanitize_text`, `sanitize_dictionary` using `bleach`.
    - `clean_json_response` attempts to repair common LLM formatting issues (strip code fences, convert single quotes to double, remove trailing commas, etc.) before JSON parsing.
    - Static serving helpers to support SPA fallback.

- `models.py`
    - Pydantic request/response models used across the API (e.g., `PromptRequest`, `CommandGenerationResponse`, `ExploitSearchResponse`, `ConfigResponse`).

- `config.py`
    - Loads `config.json` into a `ConfigResponse` Pydantic model containing `model`, `embedding_model`, `host`, and `port`.
    - The `ConfigResponse` model is defined in `models.py` and shared across the application.

## Frontend Structure: `cyber-query-ai-frontend`

- `src/app/`
  - Top-level Next App Router pages and layouts. Each feature page (e.g., `command-generation`, `script-generation`, `exploit-search`) contains the page UI and wires components together.
- `src/components/`
    - `CommandBox.tsx`, `ScriptBox.tsx`, `ExplanationBox.tsx` - present command/script output and loading states.
    - `ExploitList.tsx` - renders exploit search results (title, description/link, severity badge).
    - `Navigation.tsx`, `LanguageSelector.tsx`, `HealthIndicator.tsx` - lightweight app chrome and utilities.
- `src/lib/api.ts`
  - Single place to handle backend requests, error mapping, and timeouts (30s per request).
  - Includes `getHealth()` and `getConfig()` functions to retrieve server health and configuration.
  - Exports `useHealthStatus()` hook used by `HealthIndicator` to show online/offline state.
  - Exports `HealthStatus` type for type-safe health status handling.
  - Keep business logic out of components by using these helpers.
- `src/lib/types.ts`
  - Shared TypeScript interfaces mirroring backend Pydantic models; keep these in sync with backend models.
  - `ConfigResponse` and `HealthResponse` interfaces match backend models.
- `src/lib/sanitization.ts`
  - Client-side sanitization utilities for safe rendering
  - DOMPurify wrapper used in components that render LLM-provided HTML/code.
- `next.config.ts`
  - Reads `config.json` at build time to configure the development proxy.
  - Uses `ConfigResponse` type for type safety when parsing configuration.
  - Provides seamless proxying to backend during development.

## Operational notes

- Rate limiting: LLM endpoints limited to 5 requests/min/IP using SlowAPI.
- LLM: uses local Ollama via `langchain-ollama.OllamaLLM`.
- Sanitization: user input and LLM text sanitized with `bleach` before rendering or returning to client.
- Error reporting: server errors return HTTP 500 with a `detail` object containing `error`, `details`, and `raw` (raw LLM text when available).
