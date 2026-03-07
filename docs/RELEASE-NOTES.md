## CyberQueryAI v{{VERSION}}

**AI-powered cybersecurity assistant for ethical hacking and penetration testing**

### Quick Start

```bash
# Download and extract
wget https://github.com/{{REPOSITORY}}/releases/download/v{{VERSION}}/{{PACKAGE_NAME}}_{{VERSION}}.tar.gz
tar -xzf {{PACKAGE_NAME}}_{{VERSION}}.tar.gz
cd {{PACKAGE_NAME}}_{{VERSION}}

# Set up environment variables
cp .env.example .env

# Run the container using Docker Compose
docker compose --profile gpu up -d  # Use GPU
docker compose --profile cpu up -d  # Use CPU

# Pull required Ollama models (in a separate terminal)
# Use 'cyber-query-ai-ollama' for GPU or 'cyber-query-ai-ollama-cpu' for CPU
docker exec cyber-query-ai-ollama ollama pull mistral
docker exec cyber-query-ai-ollama ollama pull bge-m3
```

### Access Points

- **API Server**: https://localhost:443/api
- **Swagger UI**: https://localhost:443/api/docs
- **ReDoc**: https://localhost:443/api/redoc

### Documentation

- [README](https://github.com/{{REPOSITORY}}/blob/main/README.md)
- [API Documentation](https://github.com/{{REPOSITORY}}/blob/main/docs/API.md)
