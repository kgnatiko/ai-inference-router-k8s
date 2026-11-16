# AI Inference Router (Kubernetes + Helm + FastAPI + Redis)

A containerized, multi-replica inference request router packaged with a multi-stage non-root Docker build and deployed onto a 3-node Kubernetes cluster via a custom Helm chart.

## Architecture
- **API Layer (`FastAPI`):** Exposes `/health` liveness/readiness probes and `/route/{prompt_id}` request routing across multiple replicas.
- **Caching Layer (`Redis`):** Caches prompt-to-model routing decisions across pods with TTL expiration.
- **Container Hardening:** Multi-stage `python:3.12-slim` Dockerfile running as unprivileged user (`UID 10001`).
- **Orchestration:** Parameterized Helm chart (`charts/inference-router`) managing Deployments, ClusterIP Services, and health probes.

## Quickstart
```bash
docker build -t inference-router:0.1.0 .
kind load docker-image inference-router:0.1.0 --name ai-platform-lab
helm upgrade --install router ./charts/inference-router
kubectl port-forward svc/router-api-svc 8000:8000
