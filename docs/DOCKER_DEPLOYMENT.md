<!-- omit from toc -->
# Docker Deployment Guide

This guide covers CyberQueryAI-specific Docker deployment features. For general template server Docker deployment instructions (authentication, metrics, Prometheus, Grafana, basic configuration), see the [python-template-server Docker Deployment Guide](https://github.com/javidahmed64592/python-template-server/blob/main/docs/DOCKER_DEPLOYMENT.md).

<!-- omit from toc -->
## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Docker Compose Services](#docker-compose-services)
- [Ollama Integration](#ollama-integration)
  - [GPU Support (Default)](#gpu-support-default)
  - [CPU-Only Mode](#cpu-only-mode)
  - [Model Management](#model-management)
  - [Health Checks](#health-checks)
- [Multi-Stage Build Process](#multi-stage-build-process)
- [RAG System Integration](#rag-system-integration)
- [Accessing CyberQueryAI](#accessing-cyberqueryai)
  - [Web Interface](#web-interface)
  - [API Endpoints](#api-endpoints)
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

```bash
# Generate API token (if not already done)
uv sync
uv run generate-new-token

# Start all services (CyberQueryAI, Ollama, Prometheus, Grafana)
docker compose up -d

# View logs
docker compose logs -f cyber-query-ai

# Pull required models (in separate terminal)
docker exec cyber-query-ai-ollama ollama pull mistral
docker exec cyber-query-ai-ollama ollama pull bge-m3

# Access the application
# Open https://localhost:443 in your browser
# Login with the API token generated earlier

# Stop services
docker compose down
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

### GPU Support (Default)

By default, Ollama uses GPU acceleration via NVIDIA Container Toolkit:

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

**Verify GPU access:**
```bash
docker exec cyber-query-ai-ollama nvidia-smi
```

### CPU-Only Mode

For systems without GPU or CI/CD environments:

```bash
# Start with CPU profile
docker compose --profile cpu up -d

# The CPU variant uses the same image but without GPU reservations
```

### Model Management

**Required models** (configured in `configuration/config.json`):
- **LLM**: `mistral` (default, used for chat, code generation, explanations)
- **Embedding**: `bge-m3` (used for RAG vector similarity search)

**Pull models:**
```bash
# After starting containers
docker exec cyber-query-ai-ollama ollama pull mistral
docker exec cyber-query-ai-ollama ollama pull bge-m3

# List available models
docker exec cyber-query-ai-ollama ollama list

# Remove unused models
docker exec cyber-query-ai-ollama ollama rm <model-name>
```

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
- `POST /api/code-generation` - Generate security scripts
- `POST /api/code-explanation` - Explain security code
- `POST /api/exploit-search` - Search vulnerability information

**Example:**
```bash
# Health check
curl -k https://localhost:443/api/health

# Chat request
curl -k -X POST https://localhost:443/api/chat \
  -H "X-API-Key: your-token" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "How do I scan a network with nmap?"}'

# Metrics
curl -k https://localhost:443/api/metrics
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
