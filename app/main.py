import os
import socket
import redis
from fastapi import FastAPI, HTTPException

app = FastAPI(title="AI Inference Router Lab")

REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/health")
def health():
    try:
        r.ping()
        return {"status": "healthy", "redis": "connected", "pod": socket.gethostname()}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Redis unavailable: {exc}")

@app.post("/route/{prompt_id}")
def route_request(prompt_id: str, model: str = "llama-3-8b"):
    cache_key = f"route:{prompt_id}"
    cached = r.get(cache_key)
    if cached:
        return {"prompt_id": prompt_id, "routed_to": cached, "source": "redis-cache", "pod": socket.gethostname()}
    r.setex(cache_key, 300, model)
    return {"prompt_id": prompt_id, "routed_to": model, "source": "computed", "pod": socket.gethostname()}
