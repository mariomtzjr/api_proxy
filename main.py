import json
import os

import httpx
import uvicorn
from fastapi import FastAPI, Request

from .middlewares import RateLimitMiddleware
from .database import get_stats as gs

app = FastAPI()
app.add_middleware(RateLimitMiddleware)

@app.get("/proxy/{path:path}")
async def proxy(path: str, request: Request):
    target_url = f"{os.environ.get('URL_POKE_API', '')}{path}"
 
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            timeout=None
        )
        return response.json()

# Ruta para obtener las estadísticas
@app.get("/stats")
async def get_stats():
    return gs()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", log_level="info")
