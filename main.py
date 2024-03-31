import os

import httpx
import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()

app = FastAPI()

@app.get("/{path:path}")
async def proxy(path: str, request: Request):
    target_url = f"{os.environ.get('URL_POKE_API', "")}{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            timeout=None
        )
        return response.json()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", log_level="info")
