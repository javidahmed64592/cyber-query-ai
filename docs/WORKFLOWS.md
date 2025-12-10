# GitHub Workflows

This document details the CI/CD workflows to build and release the CyberQueryAI application.
They run automated code quality checks to ensure code remains robust, maintainable, and testable.

## CI Workflow

The CI workflow runs on pushes and pull requests to the `main` branch.
It consists of the following jobs:

### validate-pyproject
  - Checkout code
  - Setup Python environment with dev dependencies (via custom action)
  - Validate `pyproject.toml` structure using `validate-pyproject`

### ruff
  - Checkout code
  - Setup Python environment with dev dependencies (via custom action)
  - Run Ruff linter with `uv run -m ruff check`

### mypy
  - Checkout code
  - Setup Python environment with dev dependencies (via custom action)
  - Run mypy type checking with `uv run -m mypy .`

### pytest
  - Checkout code
  - Setup Python environment with dev dependencies (via custom action)
  - Run pytest with coverage (HTML and terminal reports) using `uv run -m pytest --cov-report html --cov-report term`
  - Fails if coverage drops below 80% (configured in `pyproject.toml`)
  - Upload HTML coverage report as artifact

### bandit
  - Checkout code
  - Setup Python environment with dev dependencies (via custom action)
  - Run security scanning with bandit on `example/` directory
  - Generate JSON report for artifacts
  - Fail if security vulnerabilities are found

### pip-audit
  - Checkout code
  - Setup Python environment with dev dependencies (via custom action)
  - Audit dependencies for known CVEs using `pip-audit --desc`

### frontend
  - Checkout code
  - Set up Node.js  and dependencies with npm caching (via custom action)
  - Run type checking with `npm run type-check`
  - Run linting with `npm run lint`
  - Run formatting check with `npm run format`
  - Run tests with `npm run test`

### version-check
  - Checkout code
  - Setup Python environment with dev dependencies (via custom action)
  - Check version consistency across `pyproject.toml`, `uv.lock`, and `cyber-query-ai-frontend/package.json`

## Build Workflow

The Build workflow runs on pushes to the `main` branch and manual dispatch, consisting of the following jobs:

### build_wheel
  - Checkout code
  - Setup Python environment with dev dependencies (via custom action)
  - Build wheel with `uv build`
  - Upload wheel artifact

### build_frontend
  - Checkout code
  - Set up Node.js  and dependencies with npm caching (via custom action)
  - Build frontend with `npm run build`
  - Upload frontend build artifact

### create_installer
  - Checkout code
  - Download backend wheel artifact
  - Download frontend build artifact
  - Prepare release directory (move wheel and static files, make scripts executable)
  - Create release tarball
  - Upload release tarball artifact

### check_installer
  - Checkout code
  - Setup Python environment with core dependencies (via custom action)
  - Download release tarball artifact
  - Extract tarball
  - Verify pre-installation directory structure
  - Run installer script
  - Verify post-installation directory structure
