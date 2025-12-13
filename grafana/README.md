<!-- omit from toc -->
# Grafana Configuration

This directory contains Grafana provisioning configuration and custom dashboards for CyberQueryAI. For detailed dashboard documentation (panels, use cases, metrics), see the [python-template-server Grafana README](https://github.com/javidahmed64592/python-template-server/blob/main/grafana/README.md).

<!-- omit from toc -->
## Table of Contents
- [Overview](#overview)
- [CyberQueryAI-Specific Configuration](#cyberqueryai-specific-configuration)
- [Available Dashboards](#available-dashboards)
- [Accessing Dashboards](#accessing-dashboards)


## Overview

CyberQueryAI uses the same Grafana dashboards as python-template-server:

1. **Health Metrics Dashboard** - Monitor server health, API token configuration, and health check performance
2. **Authentication Metrics Dashboard** - Track authentication successes/failures and detect security issues
3. **Rate Limiting & Performance Metrics Dashboard** - Monitor rate limits, API performance, and latency

For detailed information about each dashboard's panels and use cases, see the [python-template-server Grafana README](https://github.com/javidahmed64592/python-template-server/blob/main/grafana/README.md).

## CyberQueryAI-Specific Configuration

**Dashboard Folder**: `CyberQueryAI`

Configured in `provisioning/dashboards/dashboards.yml`:
```yaml
providers:
  - name: 'CyberQueryAI Dashboards'
    orgId: 1
    folder: 'CyberQueryAI'
    type: file
```

**Prometheus Scrape Target**: Uses HTTPS with self-signed certificate

Configured in `prometheus/prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'cyber-query-ai'
    scheme: https
    tls_config:
      insecure_skip_verify: true
    static_configs:
      - targets: ['cyber-query-ai:443']
    metrics_path: '/metrics'
```

## Available Dashboards

All dashboards inherit from python-template-server and work identically:

| Dashboard | UID | Path | Purpose |
|-----------|-----|------|---------|
| Health Metrics | `health-metrics` | `/d/health-metrics` | Server health and configuration monitoring |
| Authentication Metrics | `auth-metrics` | `/d/auth-metrics` | Authentication success/failure tracking |
| Rate Limiting & Performance | `rate-limit-metrics` | `/d/rate-limit-metrics` | Rate limits, API performance, and latency |

## Accessing Dashboards

1. Ensure Ollama models are pulled:
   ```bash
   docker exec cyber-query-ai-ollama ollama pull mistral
   docker exec cyber-query-ai-ollama ollama pull bge-m3
   ```

2. Start services:
   ```bash
   docker compose up -d
   ```

3. Open Grafana: http://localhost:3000

4. Login with default credentials: `admin/admin`

5. Navigate to: **Dashboards → Browse → CyberQueryAI folder**
