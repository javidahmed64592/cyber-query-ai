[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=ffd343)](https://docs.python.org/3.12/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Ollama](https://img.shields.io/badge/Ollama-AI%20Models-FF6B6B?style=flat-square&logo=ollama&logoColor=white)](https://ollama.ai/)
[![Kali Linux](https://img.shields.io/badge/Kali%20Linux-Optimized-557C94?style=flat-square&logo=kalilinux&logoColor=white)](https://www.kali.org/)
[![CI](https://img.shields.io/github/actions/workflow/status/javidahmed64592/cyber-query-ai/ci.yml?branch=main&style=flat-square&label=CI&logo=github)](https://github.com/javidahmed64592/cyber-query-ai/actions)
[![License](https://img.shields.io/github/license/javidahmed64592/cyber-query-ai?style=flat-square)](https://github.com/javidahmed64592/cyber-query-ai/blob/main/LICENSE)

<!-- omit from toc -->
# CyberQueryAI

An AI-powered cybersecurity assistant designed for ethical hacking, penetration testing, and security research. CyberQueryAI leverages advanced language models to generate commands, scripts, and insights that help cybersecurity professionals work more efficiently in controlled environments.

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
