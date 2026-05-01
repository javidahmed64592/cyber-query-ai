Software Maintenance Guide
===========================

This document outlines how to configure and setup a development environment to work on |project_name|.

Backend (Python)
----------------

.. image:: https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=ffd343
   :target: https://docs.python.org/3.13/
   :alt: Python

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=flat-square
   :target: https://github.com/astral-sh/uv
   :alt: uv

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square
   :target: https://github.com/astral-sh/ruff
   :alt: Ruff

.. image:: https://img.shields.io/badge/mypy-Latest-2A6DB2?style=flat-square
   :target: https://mypy.readthedocs.io/
   :alt: Mypy

.. image:: https://img.shields.io/badge/Sphinx-Latest-000000?style=flat-square&logo=sphinx&logoColor=white
   :target: https://www.sphinx-doc.org/
   :alt: Sphinx

.. image:: https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi&logoColor=white
   :target: https://fastapi.tiangolo.com
   :alt: FastAPI

.. image:: https://img.shields.io/badge/Langchain-Latest-1C3C3C?style=flat-square&logo=langchain&logoColor=white
   :target: https://python.langchain.com
   :alt: Langchain

Installing Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

This repository is managed using the ``uv`` Python project manager: https://docs.astral.sh/uv/

Install the required dependencies:

.. code-block:: sh

   uv sync

To include extra dependencies:

.. code-block:: sh

   uv sync --extra dev
   uv sync --extra docs
   uv sync --all-extras

Setting Up Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~

Before running the server, you need to generate an API authentication token.

.. code-block:: sh

   cp .env.example .env       # Set HOST and PORT to override defaults
   uv run generate-new-token  # Set API_TOKEN_HASH variable

This command:

- Creates a cryptographically secure token using Python's ``secrets`` module
- Hashes the token with SHA-256 for safe storage
- Stores the hash in ``.env`` file
- Displays the plain token (save it securely - it won't be shown again)

Running the Backend
~~~~~~~~~~~~~~~~~~~

**Pre-requisites:**

.. code-block:: sh

   # Ensure Ollama is running:
   ollama serve

   # Pull required models:
   ollama pull mistral
   ollama pull bge-m3

Start the server with:

.. code-block:: sh

   uv run |repo_name|

The backend will be available at ``https://localhost:443/api`` by default.

**Available Endpoints:**

- **Health Check:** ``https://localhost:443/api/health``
- **Login:** ``https://localhost:443/api/login`` (requires authentication)

**Testing the API:**

.. code-block:: sh

   curl -k https://localhost:443/api/health
   curl -k -H "X-API-Key: your-token-here" https://localhost:443/api/login

Testing, Linting, and Type Checking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

   # Lint code
   uv run ruff check .

   # Format code
   uv run ruff format .

   # Type check
   uv run mypy .

   # Run tests
   uv run pytest

   # Security scan
   uv run bandit -r |package_name|/

   # Audit dependencies
   uv run pip-audit

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

This project uses Sphinx for documentation. To build the documentation:

.. code-block:: sh

   uv run sphinx-build -M clean docs/source/ docs/build/
   uv run sphinx-build -M html docs/source/ docs/build/

The built documentation will be available at ``docs/build/html/index.html``.

----

Frontend (Next.js)
------------------

.. image:: https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black
   :target: https://reactjs.org/
   :alt: React

.. image:: https://img.shields.io/badge/Node.js-25+-339933?style=flat-square&logo=node.js&logoColor=white
   :target: https://nodejs.org/
   :alt: Node.js

.. image:: https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript&logoColor=white
   :target: https://www.typescriptlang.org/
   :alt: TypeScript

.. image:: https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js&logoColor=white
   :target: https://nextjs.org/
   :alt: Next.js

.. image:: https://img.shields.io/badge/Tailwind_CSS-4-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white
   :target: https://tailwindcss.com/
   :alt: Tailwind CSS

.. image:: https://img.shields.io/badge/ESLint-9-4B32C3?style=flat-square&logo=eslint&logoColor=white
   :target: https://eslint.org/
   :alt: ESLint

.. image:: https://img.shields.io/badge/Prettier-3-F7B93E?style=flat-square&logo=prettier&logoColor=black
   :target: https://prettier.io/
   :alt: Prettier

Ensure you run the following commands in the frontend directory:

.. code-block:: sh

   cd |repo_name|-frontend

Installing Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

Install the required dependencies using ``npm``:

.. code-block:: sh

   npm install

Running the Frontend
~~~~~~~~~~~~~~~~~~~~

Ensure the backend server is running and then start the frontend development server:

.. code-block:: sh

   npm run dev

The frontend will be available at ``http://localhost:3000``.

Testing, Linting, and Type Checking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

   # Run all quality checks
   npm run quality
   npm run quality:fix

   # Lint code
   npm run lint
   npm run lint:fix

   # Format code
   npm run format
   npm run format:fix

   # Type check
   npm run type-check

   # Run tests
   npm run test
