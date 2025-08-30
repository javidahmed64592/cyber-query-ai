[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=ffd343)](https://docs.python.org/3.12/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=for-the-badge)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

[![Ollama](https://img.shields.io/badge/Ollama-AI%20Models-FF6B6B?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.ai/)
[![Langchain](https://img.shields.io/badge/Langchain-Latest-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com/)
[![Kali Linux](https://img.shields.io/badge/Kali%20Linux-Optimized-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)](https://www.kali.org/)

[![CI](https://img.shields.io/github/actions/workflow/status/javidahmed64592/cyber-query-ai/ci.yml?branch=main&style=for-the-badge&label=CI&logo=github)](https://github.com/javidahmed64592/cyber-query-ai/actions)
[![License](https://img.shields.io/github/license/javidahmed64592/cyber-query-ai?style=for-the-badge)](https://github.com/javidahmed64592/cyber-query-ai/blob/main/LICENSE)

<!-- omit from toc -->
# Template Python Repository
This repository can be used as a template for a Python application.

<!-- omit from toc -->
## Table of Contents
- [uv](#uv)
- [Installing Dependencies](#installing-dependencies)
- [Testing, Linting, and Type Checking](#testing-linting-and-type-checking)

## uv
This repository is managed using the `uv` Python project manager: https://docs.astral.sh/uv/

To install `uv`:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh                                    # Linux/Mac
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # Windows
```

## Installing Dependencies
Install the required dependencies using `pip`:

    uv sync

To install with `dev` dependencies:

    uv sync --extra dev

## Testing, Linting, and Type Checking

- **Run tests:** `uv run pytest`
- **Lint code:** `uv run ruff check .`
- **Format code:** `uv run ruff format .`
- **Type check:** `uv run mypy .`
