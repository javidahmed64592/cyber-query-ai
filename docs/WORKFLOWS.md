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

### build_frontend
  - Checkout code
  - Set up Node.js  and dependencies with npm caching (via custom action)
  - Build frontend with `npm run build`
  - Upload frontend build artifact

### build_wheel
  - Depends on `build_frontend` job
  - Checkout code
  - Setup Python environment with core dependencies (via custom action)
  - Download frontend build artifact to `static/` directory
  - Build wheel with `uv build`
  - Inspect wheel contents for verification
  - Upload wheel artifact

### create_installer
  - Depends on `build_wheel` job
  - Checkout code
  - Download wheel artifact
  - Prepare release directory:
    - Move wheel to `release/` directory
    - Make installer script executable
    - Rename to versioned directory name
  - Create compressed tarball of release package
  - Upload release tarball artifact

### check_installer
  - Depends on `create_installer` job
  - Checkout code
  - Setup Python environment with core dependencies (via custom action)
  - Download release tarball artifact
  - Extract tarball
  - Verify pre-installation directory structure:
    - Check for wheel file, readme.txt, and executable installer script
  - Run installer script (`install_cyber_query_ai.sh`)
  - Verify post-installation directory structure:
    - Ensure virtual environment (`.venv`) created
    - Verify directories: `configuration/`, `static/`, `certs/`, `logs/`
    - Check files: `.here`, `LICENSE`, `README.md`, `SECURITY.md`, `configuration/config.json`
    - Verify SSL certificates: `certs/cert.pem`, `certs/key.pem`
    - Check executables: `cyber-query-ai`, `uninstall_cyber_query_ai.sh`
    - Ensure installer files cleaned up (wheel, readme.txt, install script removed)
