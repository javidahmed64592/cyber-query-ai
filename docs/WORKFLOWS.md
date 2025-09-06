# GitHub Workflows

This document details the CI/CD workflows to build and release the CyberQueryAI application. They run automated code quality checks to ensure code remains robust, maintainable, and testable.

## CI Workflow

The CI workflow runs on pushes and pull requests to the `main` branch.
It consists of the following jobs:

### ruff
- **Runner**: Ubuntu Latest
- **Steps**:
  - Checkout code
  - Run Ruff linter using `chartboost/ruff-action@v1`

### mypy
- **Runner**: Ubuntu Latest
- **Steps**:
  - Checkout code
  - Install uv with caching
  - Set up Python from `.python-version`
  - Install dependencies with `uv sync --extra dev`
  - Run mypy type checking with `uv run -m mypy .`

### test
- **Runner**: Ubuntu Latest
- **Steps**:
  - Checkout code
  - Install uv with caching
  - Set up Python from `.python-version`
  - Install dependencies with `uv sync --extra dev`
  - Run pytest with coverage report using `uv run -m pytest --cov-report html`
  - Upload coverage report as artifact

### frontend
- **Runner**: Ubuntu Latest
- **Working Directory**: `cyber-query-ai-frontend`
- **Steps**:
  - Checkout code
  - Set up Node.js 18 with npm caching
  - Install dependencies with `npm ci`
  - Run type checking with `npm run type-check`
  - Run linting check with `npm run lint:check`
  - Run formatting check with `npm run format:check`
  - Run tests with `npm run test`

### version-check
- **Runner**: Ubuntu Latest
- **Steps**:
  - Checkout code
  - Install uv with caching
  - Set up Python from `.python-version`
  - Set up Node.js 18
  - Install Python dependencies with `uv sync --extra dev`
  - Check version consistency across `pyproject.toml`, `uv.lock`, and `cyber-query-ai-frontend/package.json`

## Build Workflow

The Build workflow runs on pushes to the `main` branch and manual dispatch, consisting of the following jobs:

### build_wheel
- **Runner**: Ubuntu Latest
- **Steps**:
  - Checkout code
  - Install uv with caching
  - Set up Python from `.python-version`
  - Install dependencies with `uv sync --extra dev`
  - Build wheel with `uv build`
  - Upload wheel artifact

### build_frontend
- **Runner**: Ubuntu Latest
- **Steps**:
  - Checkout code
  - Set up Node.js 18 with npm caching
  - Install frontend dependencies with `npm ci` in `cyber-query-ai-frontend`
  - Build frontend with `npm run build` in `cyber-query-ai-frontend`
  - Upload frontend build artifact

### create_installer
- **Runner**: Ubuntu Latest
- **Dependencies**: `build_wheel`, `build_frontend`
- **Steps**:
  - Checkout code
  - Install uv with caching
  - Set up Python from `.python-version`
  - Download backend wheel artifact
  - Download frontend build artifact
  - Prepare release directory (move wheel and static files, make scripts executable)
  - Create release tarball
  - Upload release tarball artifact

### check_installer
- **Runner**: Ubuntu Latest
- **Dependencies**: `create_installer`
- **Steps**:
  - Checkout code
  - Install uv with caching
  - Set up Python from `.python-version`
  - Download release tarball artifact
  - Extract tarball
  - Run installer script
  - Verify installation (check for virtual environment, static directory, service scripts, config file, README, executable, uninstall script)
