# GitHub Workflows

This document details the CI/CD workflows to build and release the application.
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
- Run security scanning with bandit
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
- Check version consistency across `pyproject.toml` and `uv.lock`

## Build Workflow

The Build workflow runs on pushes and pull requests to the `main` branch.
It consists of the following jobs:

### build-frontend
- Checkout code
- Set up Node.js and dependencies with npm caching (via custom action)
- Build frontend with `npm run build`
- Upload frontend build artifact

### build-wheel
- Depends on `build-frontend` job
- Checkout code
- Setup Python environment with dev dependencies (via custom action)
- Download frontend build artifact to `static/` directory
- Build wheel with `uv build`
- Inspect wheel contents for verification
- Upload wheel artifact

### verify-structure
- Depends on `build-wheel` job
- Checkout code
- Setup Python environment (via custom action)
- Download wheel artifact
- Install wheel using `uv pip install`
- Verify installed package structure in site-packages

## Docker Workflow

The Docker workflow runs on pushes, pull requests to the `main` branch, and manual dispatch.
It consists of the following jobs:

### build-docker
- Checkout code
- Create `.env` file from `.env.example` template
- Build and start services with `docker compose up --build -d`
- Wait for services to start (5 seconds)
- Show server logs from container
- **Health check** using reusable composite action `.github/actions/docker-check-containers` with port 443
- Stop services with full cleanup: `docker compose down --volumes --remove-orphans`

### prepare-release
- Depends on `build-docker` job
- Checkout code
- Setup Python environment with dev dependencies (via custom action)
- Extract version from `pyproject.toml` using Python's `tomllib`
- Prepare release directory
- Display directory tree structure
- Create compressed tarball of the release directory
- Upload tarball as artifact

### publish-release
- Depends on `prepare-release` job
- Only runs on push to `main` branch (not PRs)
- Requires `contents: write` and `packages: write` permissions
- Checkout code
- Setup Python environment with dev dependencies (via custom action)
- Extract version from `pyproject.toml` using Python's `tomllib`
- Check if Git tag already exists (skip if duplicate)
- Download release tarball artifact
- Set up Docker Buildx for multi-platform builds
- Log in to GitHub Container Registry (ghcr.io)
- Extract Docker metadata with semantic versioning tags:
  - `v1.2.3` - Exact version
  - `1.2` - Major.minor
  - `1` - Major only
  - `latest` - Latest stable release
- Build and push multi-platform Docker images:
  - Platforms: `linux/amd64`, `linux/arm64`
  - Registry: `ghcr.io/<owner>/<repo>`
  - Uses GitHub Actions cache for layer caching
- Generate release notes
- Create GitHub Release with version tag and release notes
