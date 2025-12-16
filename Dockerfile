# Multi-stage Dockerfile for CyberQueryAI
# Stage 1: Frontend build stage - build Next.js static export
FROM node:22-alpine AS frontend-builder

WORKDIR /frontend

# Copy frontend package files
COPY cyber-query-ai-frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY cyber-query-ai-frontend/ ./

# Build static export
RUN npm run build

# Stage 2: Backend build stage - build wheel using uv
FROM python:3.13-slim AS backend-builder

WORKDIR /build

# Install Git for dependency resolution
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy backend source files
COPY cyber_query_ai/ ./cyber_query_ai/
COPY configuration/ ./configuration/
COPY grafana/ ./grafana/
COPY prometheus/ ./prometheus/
COPY rag_data/ ./rag_data/
COPY pyproject.toml .here LICENSE README.md SECURITY.md ./

# Copy built frontend from previous stage
COPY --from=frontend-builder /frontend/out ./static/

# Build the wheel
RUN uv build --wheel

# Stage 3: Runtime stage
FROM python:3.13-slim

WORKDIR /app

# Install Git and wget for dependency resolution and model checking
RUN apt-get update && apt-get install -y git wget && rm -rf /var/lib/apt/lists/*

# Install uv in runtime stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the built wheel from backend builder
COPY --from=backend-builder /build/dist/*.whl /tmp/

# Install the wheel
RUN uv pip install --system --no-cache /tmp/*.whl && \
    rm /tmp/*.whl

# Create required directories
RUN mkdir -p /app/logs /app/certs

# Copy included files from installed wheel to app directory
RUN SITE_PACKAGES_DIR=$(find /usr/local/lib -name "site-packages" -type d | head -1) && \
    cp -r "${SITE_PACKAGES_DIR}/configuration" /app/ && \
    cp -r "${SITE_PACKAGES_DIR}/grafana" /app/ && \
    cp -r "${SITE_PACKAGES_DIR}/prometheus" /app/ && \
    cp -r "${SITE_PACKAGES_DIR}/static" /app/ && \
    cp -r "${SITE_PACKAGES_DIR}/rag_data" /app/ && \
    cp "${SITE_PACKAGES_DIR}/.here" /app/.here && \
    cp "${SITE_PACKAGES_DIR}/LICENSE" /app/LICENSE && \
    cp "${SITE_PACKAGES_DIR}/README.md" /app/README.md && \
    cp "${SITE_PACKAGES_DIR}/SECURITY.md" /app/SECURITY.md

# Create startup script with Ollama model checking
RUN echo '#!/bin/sh\n\
    set -e\n\
    \n\
    # Generate API token if needed\n\
    if [ -z "$API_TOKEN_HASH" ]; then\n\
    echo "Generating new token..."\n\
    generate-new-token\n\
    export $(grep -v "^#" .env | xargs)\n\
    fi\n\
    \n\
    # Generate certificates if needed\n\
    if [ ! -f certs/cert.pem ] || [ ! -f certs/key.pem ]; then\n\
    echo "Generating self-signed certificates..."\n\
    generate-certificate\n\
    fi\n\
    \n\
    # Check required Ollama models\n\
    REQUIRED_MODELS="mistral bge-m3"\n\
    \n\
    echo "Checking Ollama connection at $OLLAMA_HOST..."\n\
    MAX_RETRIES=30\n\
    RETRY_COUNT=0\n\
    \n\
    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do\n\
    if wget -q -O- "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; then\n\
    echo "Ollama is ready"\n\
    break\n\
    fi\n\
    echo "Waiting for Ollama... ($((RETRY_COUNT + 1))/$MAX_RETRIES)"\n\
    sleep 2\n\
    RETRY_COUNT=$((RETRY_COUNT + 1))\n\
    done\n\
    \n\
    if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then\n\
    echo "WARNING: Could not connect to Ollama. Application will start but may not function properly."\n\
    else\n\
    MODELS_JSON=$(wget -q -O- "$OLLAMA_HOST/api/tags")\n\
    \n\
    # Extract model names from configuration file\n\
    CONFIG_MODEL=$(python -c "import json; print(json.load(open('\''configuration/cyber_query_ai_config.json'\''))['\''model'\'']['\''model'\''])")\n\
    CONFIG_EMBEDDING_MODEL=$(python -c "import json; print(json.load(open('\''configuration/cyber_query_ai_config.json'\''))['\''model'\'']['\''embedding_model'\''])")\n\
    \n\
    # Check models from configuration file\n\
    if ! echo "$MODELS_JSON" | grep -q "${CONFIG_MODEL}:latest"; then\n\
    echo "⚠ Model $CONFIG_MODEL not found. Pull with: docker exec cyber-query-ai-ollama ollama pull $CONFIG_MODEL"\n\
    fi\n\
    \n\
    if ! echo "$MODELS_JSON" | grep -q "${CONFIG_EMBEDDING_MODEL}:latest"; then\n\
    echo "⚠ Model $CONFIG_EMBEDDING_MODEL not found. Pull with: docker exec cyber-query-ai-ollama ollama pull $CONFIG_EMBEDDING_MODEL"\n\
    fi\n\
    fi\n\
    \n\
    exec cyber-query-ai' > /app/start.sh && \
    chmod +x /app/start.sh

# Expose HTTPS port
EXPOSE 443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('https://localhost:443/api/health', context=__import__('ssl')._create_unverified_context()).read()" || exit 1

CMD ["/app/start.sh"]
