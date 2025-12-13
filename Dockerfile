# Multi-stage Dockerfile for CyberQueryAI
# Stage 1: Frontend build stage - build Next.js static export
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend

# Copy frontend package files
COPY cyber-query-ai-frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY cyber-query-ai-frontend/ ./
COPY configuration/config.json ../configuration/config.json

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
COPY rag_data/ ./rag_data/
COPY pyproject.toml .here LICENSE README.md SECURITY.md ./

# Copy built frontend from previous stage
COPY --from=frontend-builder /frontend/out ./static/

# Build the wheel
RUN uv build --wheel

# Stage 3: Runtime stage
FROM python:3.13-slim

# Build arguments for environment-specific config
ARG ENV=dev
ARG PORT=443

WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 cyberqueryai_user && \
    chown -R cyberqueryai_user:cyberqueryai_user /app

# Install Git for dependency resolution
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install uv in runtime stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the built wheel from backend builder
COPY --from=backend-builder /build/dist/*.whl /tmp/

# Install the wheel
RUN uv pip install --system --no-cache /tmp/*.whl && \
    rm /tmp/*.whl

# Create required directories
RUN mkdir -p /app/configuration /app/logs /app/certs

# Copy included files from installed wheel to app directory
RUN SITE_PACKAGES_DIR=$(find /usr/local/lib -name "site-packages" -type d | head -1) && \
    cp "${SITE_PACKAGES_DIR}/.here" /app/.here && \
    cp -r "${SITE_PACKAGES_DIR}/configuration" /app/ && \
    cp -r "${SITE_PACKAGES_DIR}/static" /app/ && \
    cp -r "${SITE_PACKAGES_DIR}/rag_data" /app/ && \
    cp "${SITE_PACKAGES_DIR}/LICENSE" /app/LICENSE && \
    cp "${SITE_PACKAGES_DIR}/README.md" /app/README.md && \
    cp "${SITE_PACKAGES_DIR}/SECURITY.md" /app/SECURITY.md && \
    chown -R cyberqueryai_user:cyberqueryai_user /app

# Create startup script
RUN echo '#!/bin/sh\n\
    if [ ! -f .env ]; then\n\
    echo "Generating new token..."\n\
    generate-new-token\n\
    export $(grep -v "^#" .env | xargs)\n\
    fi\n\
    if [ ! -f certs/cert.pem ] || [ ! -f certs/key.pem ]; then\n\
    echo "Generating self-signed certificates..."\n\
    generate-certificate\n\
    fi\n\
    exec cyber-query-ai' > /app/start.sh && \
    chmod +x /app/start.sh && \
    chown cyberqueryai_user:cyberqueryai_user /app/start.sh

# Switch to non-root user
USER cyberqueryai_user

# Expose HTTPS port
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('https://localhost:$PORT/api/health', context=__import__('ssl')._create_unverified_context()).read()" || exit 1

CMD ["/app/start.sh"]
