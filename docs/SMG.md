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

## Backend (Python)

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=ffd343)](https://docs.python.org/3.12/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=flat-square)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Langchain](https://img.shields.io/badge/Langchain-Latest-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://python.langchain.com/)

### Directory Structure

```
cyber_query_ai/
├── api.py          # FastAPI endpoints
├── chatbot.py      # LLM integration
├── config.py       # Configuration management
├── helpers.py      # Utility functions
├── main.py         # Application entry point
└── models.py       # Pydantic models
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

### Running the Backend

Start the FastAPI server:

```sh
uv run cyber-query-ai
```

The backend will be available at `http://localhost:8000` by default.

### Testing, Linting, and Type Checking

- **Run tests:** `uv run pytest`
- **Lint code:** `uv run ruff check .`
- **Format code:** `uv run ruff format .`
- **Type check:** `uv run mypy .`

## Frontend (TypeScript)

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
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
│   │   ├── command-explanation/ # Command explanation interface
│   │   ├── command-generation/  # Command generation interface
│   │   ├── exploit-search/      # Exploit search interface
│   │   ├── script-explanation/  # Script explanation interface
│   │   ├── script-generation/   # Script generation interface
│   │   ├── globals.css          # UI style configuration
│   │   ├── layout.tsx           # Root layout with navigation
│   │   └── page.tsx             # Homepage (redirects to command-generation)
│   ├── components/
│   │   ├── CommandBox.tsx       # Generated command display
│   │   ├── ExplanationBox.tsx   # AI explanation display
│   │   ├── ExploitList.tsx      # Exploit references display
│   │   ├── HealthIndicator.tsx  # Server health status indicator
│   │   ├── LanguageSelector.tsx # Dropdown for language selection
│   │   ├── Navigation.tsx       # Main navigation bar
│   │   ├── ScriptBox.tsx        # Generated script display
│   │   └── TextInput.tsx        # Text input component
│   ├── lib/
│   │   ├── api.ts               # API communication functions
│   │   ├── sanitization.ts      # Input sanitization utilities
│   │   ├── types.ts             # TypeScript type definitions
│   │   ├── useHealthStatus.ts   # Hook for server health status
│   │   └── version.ts           # Application versioning
├── jest.config.js               # Jest configuration for testing
├── jest.setup.js                # Jest setup for mocking and environment
├── next.config.ts               # Next.js configuration
├── package.json                 # Dependencies and scripts
└── postcss.config.js            # Tailwind CSS configuration
```

### Installing Dependencies

Install the required dependencies:

```bash
npm install
```

### Running the Frontend

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

### Testing, Linting, and Type Checking

- **Run tests:** `npm run test`
- **Run all quality checks:** `npm run quality`
- **Fix all quality issues:** `npm run quality:fix`
- **Lint code:** `npm run lint:check`
- **Fix lint issues:** `npm run lint`
- **Format code:** `npm run format`
- **Check formatting:** `npm run format:check`
- **Type check:** `npm run type-check`
