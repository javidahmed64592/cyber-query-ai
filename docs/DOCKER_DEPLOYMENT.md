<!-- omit from toc -->
# Docker Deployment Guide

This guide covers CyberQueryAI-specific Docker deployment features. For general template server Docker deployment instructions (authentication, metrics, Prometheus, Grafana, basic configuration), see the [python-template-server Docker Deployment Guide](https://github.com/javidahmed64592/python-template-server/blob/main/docs/DOCKER_DEPLOYMENT.md).

<!-- omit from toc -->
## Table of Contents
- [The CPU variant uses the same image but without GPU reservations](#the-cpu-variant-uses-the-same-image-but-without-gpu-reservations)
    - [Volume Management](#volume-management)
    - [Health Checks](#health-checks)
  - [Multi-Stage Build Process](#multi-stage-build-process)
  - [RAG System Integration](#rag-system-integration)
  - [Accessing CyberQueryAI](#accessing-cyberqueryai)
    - [Web Interface](#web-interface)
    - [API Endpoints](#api-endpoints)
  - [GitHub Container Registry](#github-container-registry)
    - [Available Images](#available-images)
    - [Pulling Images](#pulling-images)
    - [Using with Docker Compose](#using-with-docker-compose)
  - [Troubleshooting](#troubleshooting)
    - [Ollama Connection Issues](#ollama-connection-issues)
    - [Missing Models](#missing-models)
    - [GPU Not Available](#gpu-not-available)
    - [Frontend Not Loading](#frontend-not-loading)
    - [RAG System Errors](#rag-system-errors)
    - [LLM Responses Slow or Timeout](#llm-responses-slow-or-timeout)

## Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **NVIDIA GPU** (optional, for GPU acceleration)
- **NVIDIA Container Toolkit** (optional, for GPU support)

## Quick Start

### Using Pre-built Image (Recommended)

CyberQueryAI releases are automatically published to GitHub Container Registry as multi-platform Docker images:

```bash
# Download docker-compose.yml from the repository
curl -O https://raw.githubusercontent.com/javidahmed64592/cyber-query-ai/main/docker-compose.yml

# Start all services (automatically pulls ghcr.io/javidahmed64592/cyber-query-ai:latest)
# For GPU systems:
docker compose --profile gpu up -d

# For CPU-only systems:
docker compose --profile cpu up -d

# Optional: Use a specific version instead of latest
export CYBER_QUERY_AI_IMAGE=ghcr.io/javidahmed64592/cyber-query-ai:v1.0.4
docker compose --profile gpu up -d

# View logs
docker compose logs -f cyber-query-ai

# Pull required Ollama models (in a separate terminal)
# Use 'cyber-query-ai-ollama' for GPU or 'cyber-query-ai-ollama-cpu' for CPU
docker exec cyber-query-ai-ollama ollama pull mistral
docker exec cyber-query-ai-ollama ollama pull bge-m3

# Access the application at https://localhost:443
```

**Note:**
- The container automatically generates an API token and SSL certificates on first run if the `API_TOKEN_HASH` environment variable has not been set.
- The Ollama service does not automatically pull models - you must manually pull the required models (`mistral` and `bge-m3`) as shown above.
- By default, docker-compose.yml pulls `ghcr.io/javidahmed64592/cyber-query-ai:latest`. Set `CYBER_QUERY_AI_IMAGE` environment variable to use a specific version.

### Building from Source

For development or customization:

```bash
# Clone the repository
git clone https://github.com/javidahmed64592/cyber-query-ai.git
cd cyber-query-ai

# (Optional) Generate persistent API token for development
# If skipped, Docker will auto-generate a new token on each restart
uv sync
uv run generate-new-token

# Build and start all services
# For GPU systems:
docker compose --profile gpu up --build -d

# For CPU-only systems:
docker compose --profile cpu up --build -d

# View logs
docker compose logs -f cyber-query-ai

# Pull required Ollama models
# Use 'cyber-query-ai-ollama' for GPU or 'cyber-query-ai-ollama-cpu' for CPU
docker exec cyber-query-ai-ollama ollama pull mistral
docker exec cyber-query-ai-ollama ollama pull bge-m3

# Access the application at https://localhost:443
# Login with the API token generated earlier

# Stop services (include the profile used)
docker compose --profile gpu down --volumes --remove-orphans
# or for CPU:
# docker compose --profile cpu down --volumes --remove-orphans
```

## Docker Compose Services

CyberQueryAI extends the template server with four services:

1. **cyber-query-ai-ollama** (Port 11434)
   - Local LLM inference engine with GPU support
   - Serves both the main LLM (`mistral`) and embedding model (`bge-m3`)
   - Persistent model storage via Docker volume
   - Health checks ensure models are available

2. **cyber-query-ai** (Port 443)
   - FastAPI application with HTTPS serving Next.js frontend and API
   - Extends python-template-server with cybersecurity-specific endpoints
   - RAG-enhanced prompts for tool documentation
   - Auto-generates certificates and API tokens on first run

3. **cyber-query-ai-prometheus** (Port 9090)
   - Inherits template server metrics plus custom CyberQueryAI metrics
   - Scrapes `/api/metrics` endpoint

4. **cyber-query-ai-grafana** (Port 3000)
   - Pre-configured with authentication, rate limiting, and health dashboards
   - Custom dashboard for CyberQueryAI-specific metrics

## Ollama Integration

### GPU Support

For systems with NVIDIA GPU and Container Toolkit, use the `gpu` profile:

```bash
# Use GPU profile for NVIDIA GPU acceleration
docker compose --profile gpu up -d
```

This configuration uses:

```yaml
services:
  cyber-query-ai-ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

### CPU-Only Mode

For systems without NVIDIA GPU or in CI/CD environments, use the `cpu` profile:

```bash
# Use CPU profile for systems without GPU
docker compose --profile cpu up -d
```

**Important Notes:**
- Both GPU and CPU modes require explicit profile selection
- GPU profile: Container name is `cyber-query-ai-ollama`
- CPU profile: Container name is `cyber-query-ai-ollama-cpu`
- Both services use the network alias `ollama` for internal communication

**Verify GPU access (GPU mode only):**
```bash
docker exec cyber-query-ai-ollama nvidia-smi
```

# The CPU variant uses the same image but without GPU reservations
```

### Model Management

**Required models must be manually pulled.** The application will not function without these models:

**Required models** (configured in `configuration/config.json`):
- **LLM**: `mistral` (default, used for chat, code generation, explanations)
- **Embedding**: `bge-m3` (used for RAG vector similarity search)

**Pull models:**
```bash
# After starting containers, pull required models
docker exec cyber-query-ai-ollama ollama pull mistral
docker exec cyber-query-ai-ollama ollama pull bge-m3

# List available models
docker exec cyber-query-ai-ollama ollama list

# Remove unused models
docker exec cyber-query-ai-ollama ollama rm <model-name>
```

### Volume Management

The docker-compose configuration uses **named volumes** to persist runtime data while preserving built-in defaults:

**Named volumes (automatically managed):**
- `cyber-query-ai-certs` - SSL certificates (auto-generated on first run)
- `cyber-query-ai-logs` - Application logs
- `ollama-data` - Downloaded Ollama models
- `prometheus-data` - Prometheus metrics
- `grafana-data` - Grafana dashboards and settings

**Configuration customization (development only):**

By default, the application uses the `config.json` and RAG data built into the Docker image. To customize these files:

1. **Extract default configuration:**
   ```bash
   # Copy config from container to local directory
   docker cp cyber-query-ai:/app/configuration ./configuration
   docker cp cyber-query-ai:/app/rag_data ./rag_data
   ```

2. **Edit docker-compose.yml to mount local directories:**
   ```yaml
   services:
     cyber-query-ai:
       volumes:
         - cyber-query-ai-certs:/app/certs
         - cyber-query-ai-logs:/app/logs
   ```

3. **Restart the container:**
   ```bash
   docker compose --profile gpu restart cyber-query-ai
   ```

**Warning:** Mounting local directories will override the built-in configuration. If the local directories are empty, the application will fail to start.

### Health Checks

All services include health checks with retry logic:

```yaml
healthcheck:
  test: ["CMD", "ollama", "list"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

The main application waits up to 60 seconds for Ollama to be ready before starting.

## Multi-Stage Build Process

The Dockerfile uses three stages to optimize image size:

**Stage 1: Frontend Build**
- Node.js 20 Alpine image
- Builds Next.js static export (`npm run build`)
- Output: `out/` directory with static HTML/JS/CSS

**Stage 2: Backend Build**
- Python 3.13 slim image with uv
- Builds Python wheel from source
- Includes pre-built frontend from Stage 1

**Stage 3: Runtime**
- Python 3.13 slim (minimal dependencies)
- Installs wheel and extracts static files to `/app/static/`
- Creates startup script with Ollama connection retry and model checking
- Final image includes:
  - Backend API server
  - Static frontend files
  - RAG data for tool documentation
  - Configuration templates

## RAG System Integration

The RAG (Retrieval-Augmented Generation) system enhances LLM prompts with relevant cybersecurity tool documentation:

**Volume mount:**
```yaml
volumes:
  - ./rag_data:/app/rag_data
```

**Contents:**
- `rag_data/tools.json`: Metadata mapping (tool names, categories, tags)
- `rag_data/*.txt`: Tool documentation files

The RAG system uses the `bge-m3` embedding model to find the top-3 most relevant tool documents for each user prompt.

## Accessing CyberQueryAI

### Web Interface

**Base URL:** `https://localhost:443` (self-signed certificate)

**Pages:**
- **Login**: `/login` - API key authentication
- **Chat Assistant**: `/assistant` - Conversational AI for security advice
- **Code Generation**: `/code-generation` - Generate Bash/Python/PowerShell scripts
- **Code Explanation**: `/code-explanation` - Explain existing security scripts
- **Exploit Search**: `/exploit-search` - Query ExploitDB-style vulnerability info

### API Endpoints

All endpoints require `X-API-Key` header except where noted:

**Public:**
- `GET /api/health` - Health status (no auth)
- `GET /api/config` - Model configuration and version (no auth)
- `GET /api/metrics` - Prometheus metrics (no auth)

**Authenticated:**
- `POST /api/chat` - Chat with LLM (RAG-enhanced)

## GitHub Container Registry

CyberQueryAI Docker images are automatically published to GitHub Container Registry on every release.

### Available Images

**Registry:** `ghcr.io/javidahmed64592/cyber-query-ai`

**Tags:**
- `latest` - Most recent stable release (recommended)
- `v1.2.3` - Specific semantic version
- `1.2` - Major.minor version (receives patch updates)
- `1` - Major version only (receives minor and patch updates)

**Platforms:**
- `linux/amd64` (Intel/AMD 64-bit)
- `linux/arm64` (ARM 64-bit, e.g., Apple Silicon, Raspberry Pi)

### Pulling Images

```bash
# Pull latest release
docker pull ghcr.io/javidahmed64592/cyber-query-ai:latest

# Pull specific version
docker pull ghcr.io/javidahmed64592/cyber-query-ai:v0.1.0

# Pull major version (gets updates automatically)
docker pull ghcr.io/javidahmed64592/cyber-query-ai:0
```

### Using with Docker Compose

The `docker-compose.yml` file supports both pulling pre-built images and building from source via the `CYBER_QUERY_AI_IMAGE` environment variable:

**Default behavior** (pulls latest pre-built image):
```bash
# Uses ghcr.io/javidahmed64592/cyber-query-ai:latest by default
docker compose --profile gpu up -d
```

**Use specific version:**
```bash
# Set environment variable to use a specific version
export CYBER_QUERY_AI_IMAGE=ghcr.io/javidahmed64592/cyber-query-ai:v1.0.4
docker compose --profile gpu up -d
```

**Build from source** (for development):
```bash
# Use --build flag to force building from Dockerfile instead of pulling
docker compose --profile gpu up --build -d
```

## Troubleshooting

### Ollama Connection Issues

**Symptom:** `WARNING: Could not connect to Ollama`

**Check Ollama service:**
```bash
# View Ollama logs
docker compose logs cyber-query-ai-ollama

# Check if Ollama is responding
docker exec cyber-query-ai-ollama ollama list

# Restart Ollama
docker compose restart cyber-query-ai-ollama
```

**Verify network connectivity:**
```bash
# From main container
docker exec cyber-query-ai wget -O- http://cyber-query-ai-ollama:11434/api/tags
```

### Missing Models

**Symptom:** Warnings like `⚠ Model mistral not found`

**Pull models:**
```bash
docker exec cyber-query-ai-ollama ollama pull mistral
docker exec cyber-query-ai-ollama ollama pull bge-m3
```

**Verify models:**
```bash
docker exec cyber-query-ai-ollama ollama list
# Should show:
# NAME                    ID              SIZE      MODIFIED
# mistral:latest          ...             ...       ...
# bge-m3:latest           ...             ...       ...
```

### GPU Not Available

**Symptom:** Ollama falls back to CPU, very slow responses

**Check NVIDIA drivers:**
```bash
nvidia-smi
```

**Check Docker GPU support:**
```bash
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

**If GPU unavailable:**
```bash
# Use CPU profile instead
docker compose --profile cpu up -d
```

### Frontend Not Loading

**Symptom:** 404 errors or blank pages

**Verify static files:**
```bash
docker exec cyber-query-ai ls -la /app/static/
# Should show:
# index.html, _next/, manifest.json, etc.
```

**Check build logs:**
```bash
docker compose logs cyber-query-ai | grep -i "frontend"
```

**Rebuild with no cache:**
```bash
docker compose build --no-cache cyber-query-ai
docker compose up -d
```

### RAG System Errors

**Symptom:** LLM responses don't include tool documentation

**Check RAG data:**
```bash
docker exec cyber-query-ai ls -la /app/rag_data/
# Should show:
# tools.json, nmap.txt, metasploit.txt, etc.
```

**Verify embedding model:**
```bash
docker exec cyber-query-ai-ollama ollama list | grep bge-m3
```

**Check logs for RAG errors:**
```bash
docker compose logs cyber-query-ai | grep -i "rag\|embed"
```

### LLM Responses Slow or Timeout

**Check resource usage:**
```bash
docker stats cyber-query-ai-ollama
```

**Monitor Ollama processing:**
```bash
docker compose logs -f cyber-query-ai-ollama
```

**Recommendations:**
- **GPU mode**: Ensure GPU is accessible and not used by other processes
- **CPU mode**: Increase CPU limits or use a smaller model
- **Timeout**: Increase timeout in `cyber-query-ai-frontend/src/lib/api.ts`

**Optimize for CPU:**
```bash
# Use a smaller model (edit configuration/config.json)
docker exec cyber-query-ai-ollama ollama pull mistral:7b-instruct-q4_0
```

Then update `configuration/config.json`:
```json
{
  "model": {
    "model": "mistral:7b-instruct-q4_0"
  }
}
```

Restart: `docker compose restart cyber-query-ai`
