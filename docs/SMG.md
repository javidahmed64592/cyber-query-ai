<!-- omit from toc -->
# Software Maintenance Guide

This document outlines how to configure and setup a development environment to work on the CyberQueryAI application.

<!-- omit from toc -->
## Table of Contents
- [Backend (Python)](#backend-python)
  - [Directory Structure](#directory-structure)
  - [Installing Dependencies](#installing-dependencies)
  - [Running the Backend](#running-the-backend)
  - [Testing, Linting, and Type Checking](#testing-linting-and-type-checking)
- [Frontend (TypeScript)](#frontend-typescript)
  - [Directory Structure](#directory-structure-1)
  - [Installing Dependencies](#installing-dependencies-1)
  - [Running the Frontend](#running-the-frontend)
  - [Testing, Linting, and Type Checking](#testing-linting-and-type-checking-1)
- [Creating a New Release Version](#creating-a-new-release-version)
  - [Steps to Update Version](#steps-to-update-version)

## Backend (Python)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=ffd343)](https://docs.python.org/3.13/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=flat-square)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Langchain](https://img.shields.io/badge/Langchain-Latest-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://python.langchain.com/)

### Directory Structure

```
cyber_query_ai/
├── server.py       # CyberQueryAIServer class (extends TemplateServer)
├── chatbot.py      # LLM integration with RAG support
├── helpers.py      # Utility functions (sanitization, JSON cleaning, static file serving, filepath helpers)
├── main.py         # Application entry point
├── models.py       # Pydantic models (requests, responses, config)
└── rag.py          # RAG system with semantic search
```

### Installing Dependencies

This repository is managed using the `uv` Python project manager: https://docs.astral.sh/uv/

To install `uv`:

```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # Windows
```

Install the required dependencies:

```sh
uv sync
```

To include development dependencies:

```sh
uv sync --extra dev
```

After installing dev dependencies, set up pre-commit hooks:

```sh
    uv run pre-commit install
```

### Running the Backend

**Prerequisites:**
1. Ensure Ollama is running:
   ```sh
   ollama serve
   ```

2. Pull required models:
   ```sh
   ollama pull mistral
   ollama pull bge-m3
   ```

3. Generate API authentication token:
   ```sh
   uv run generate-new-token
   # Save the displayed token for authentication!
   ```

4. Generate SSL certificate (optional, auto-generated on first run):
   ```sh
   uv run generate-certificate
   ```

**Configuration:**
Edit `configuration/config.json` to customize server settings:
```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 443
  },
  "model": {
    "model": "mistral",
    "embedding_model": "bge-m3"
  },
  "rate_limit": {
    "enabled": true,
    "rate_limit": "10/minute"
  }
}
```

**Start the server:**
```sh
uv run cyber-query-ai
```

The backend will be available at `https://localhost:443` by default (HTTPS only).

### Testing, Linting, and Type Checking

- **Run all pre-commit checks:** `uv run pre-commit run --all-files`
- **Lint code:** `uv run ruff check .`
- **Format code:** `uv run ruff format .`
- **Type check:** `uv run mypy .`
- **Run tests:** `uv run pytest`
- **Security scan:** `uv run bandit -r cyber_query_ai/`
- **Audit dependencies:** `uv run pip-audit`


## Frontend (TypeScript)

[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat-square&logo=node.js&logoColor=white)](https://nodejs.org/)
[![ESLint](https://img.shields.io/badge/ESLint-9-4B32C3?style=flat-square&logo=eslint&logoColor=white)](https://eslint.org/)
[![Prettier](https://img.shields.io/badge/Prettier-3-F7B93E?style=flat-square&logo=prettier&logoColor=black)](https://prettier.io/)

### Directory Structure

```
cyber-query-ai-frontend/
├── src/
│   ├── app/
│   │   ├── about/               # About page
│   │   ├── code-explanation/    # Code explanation interface
│   │   ├── code-generation/     # Code generation interface
│   │   ├── exploit-search/      # Exploit search interface
│   │   ├── login/               # Login page for API key authentication
│   │   ├── 404/                 # Custom 404 page
│   │   ├── globals.css          # UI style configuration
│   │   ├── layout.tsx           # Root layout with AuthProvider and navigation
│   │   ├── not-found.tsx        # Not found page
│   │   └── page.tsx             # Homepage (AI Assistant with conversational chat)
│   ├── components/
│   │   ├── ChatMessage.tsx      # Individual message rendering with code blocks
│   │   ├── ChatWindow.tsx       # Conversational chat interface
│   │   ├── ErrorNotification.tsx # Portal-based error notifications
│   │   ├── ExplanationBox.tsx   # AI explanation display
│   │   ├── ExploitList.tsx      # Exploit references display
│   │   ├── Footer.tsx           # App footer with version info
│   │   ├── HealthIndicator.tsx  # Server health status indicator
│   │   ├── Navigation.tsx       # Main navigation bar with logout
│   │   ├── ScriptBox.tsx        # Generated code display
│   │   └── TextInput.tsx        # Text input component
│   ├── contexts/
│   │   └── AuthContext.tsx      # Authentication context and route protection
│   ├── lib/
│   │   ├── api.ts               # API client with authentication interceptors
│   │   ├── auth.ts              # localStorage API key management
│   │   ├── sanitization.ts      # Input/output sanitization utilities
│   │   └── types.ts             # TypeScript type definitions (matches backend models)
├── jest.config.js               # Jest configuration for testing
├── jest.setup.js                # Jest setup for mocking and environment
├── next.config.ts               # Next.js configuration
├── package.json                 # Dependencies and scripts
└── postcss.config.mjs           # Tailwind CSS configuration
```

### Installing Dependencies

Install the required dependencies:

```bash
npm install
```

### Running the Frontend

**Prerequisites:**
Ensure the backend server is running (see [Running the Backend](#running-the-backend))

**Start the development server:**
```bash
cd cyber-query-ai-frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`.

**Authentication in Development:**
- The development server proxies `/api` requests to the HTTPS backend (`https://localhost:443`)
- On first visit, you'll be redirected to `/login/`
- Enter the API token generated via `uv run generate-new-token`
- The token is stored in localStorage and included in all API requests via the `X-API-KEY` header

**Building for Production:**
```bash
npm run build        # Standard Next.js build
npm run build:static # Static export to ../static/ directory
```

### Testing, Linting, and Type Checking

- **Run tests:** `npm run test`
- **Run all quality checks:** `npm run quality`
- **Fix all quality issues:** `npm run quality:fix`
- **Type check:** `npm run type-check`
- **Lint code:** `npm run lint`
- **Fix lint issues:** `npm run lint:fix`
- **Check formatting:** `npm run format`
- **Format code:** `npm run format:fix`

## Creating a New Release Version

When preparing a new release, you must update version numbers across multiple files to maintain consistency. The CI pipeline enforces version alignment between backend and frontend.

### Steps to Update Version

1. **Update `pyproject.toml`** (backend version):
   ```toml
   [project]
   name = "cyber-query-ai"
   version = "X.Y.Z"  # Update this line
   ```

2. **Update `cyber-query-ai-frontend/package.json`** (frontend version):
   ```json
   {
     "name": "cyber-query-ai-frontend",
     "version": "X.Y.Z"  // Update this line to match backend
   }
   ```

3. **Synchronize `uv.lock`** (from project root):
   ```sh
   uv lock
   ```

4. **Synchronize `package-lock.json`** (from `cyber-query-ai-frontend` directory):
   ```sh
   cd cyber-query-ai-frontend
   npm install --package-lock-only
   ```
