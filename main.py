import json
import os

import httpx
import uvicorn
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from .middlewares import RateLimitMiddleware
from .database import (
    get_stats as gs,
    get_data_from_redis,
    store_data_in_redis
)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(RateLimitMiddleware)

@app.get("/proxy/{path:path}")
@limiter.limit(os.environ.get('RATE_LIMIT'))
async def proxy(path: str, request: Request):
    target_url = f"{os.environ.get('URL_MELI_API', '')}{path}"
 
    # Verificar si la respuesta está en caché en Redis
    cached_response = get_data_from_redis(path)
    if cached_response:
        return cached_response
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            timeout=None
        )
        # Almacenar la respuesta en caché en Redis
        store_data_in_redis(path, response.json())
        return response.json()

# Ruta para obtener las estadísticas
@app.get("/stats")
async def get_stats():
    return gs()

@app.get("/redis/{path: path}")
async def get_redis_data(path: str):
    return store_data_in_redis(path)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", log_level="info")
