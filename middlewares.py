from datetime import datetime
import asyncio
from collections import defaultdict

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .database import (
    get_request_count_by_ip,
    get_request_count_by_path,
    log_request
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit_per_ip: int = 10, limit_per_path: int = 5):
        super().__init__(app)
        self.limit_per_ip = limit_per_ip
        self.limit_per_path = limit_per_path

    async def dispatch(self, request, call_next):
        remote_ip = request.client.host
        request_path = request.url.path

        request_count_ip = get_request_count_by_ip(remote_ip)
        request_count_path = get_request_count_by_path(request_path)

        if  request_count_ip >= self.limit_per_ip:
            return Response(f"Too Many Requests: {request_count_ip}", status_code=429)
        elif request_count_path >= self.limit_per_path:
            return Response (f"Too Many Path Requests: {request_count_path}", status_code=429)

        log_request(remote_ip, request_path)
        response = await call_next(request)
        return response
