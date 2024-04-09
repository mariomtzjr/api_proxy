import os

from fastapi import HTTPException
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Configuración del secret key para el token
SECRET_KEY = os.environ.get("SECRET_KEY", "")
serializer = Serializer(SECRET_KEY)  # El token expira en 60 segundos

from .database.database import DBManager


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit_per_path: int = 10):
        super().__init__(app)
        self.limit_per_path = limit_per_path
        self.db_service = DBManager()

    async def dispatch(self, request, call_next):
        request_path = request.url.path
        remote_ip = request.client.host
        request_count_path = self.db_service.get_request_count_by_path(request_path)

        # Verificar si se incluye el token de autenticación en el encabezado de la solicitud
        # if "Authorization" not in request.headers:
        #     raise HTTPException(status_code=401, detail="Missing Authorization header")

        # # Obtener el token de autenticación del encabezado
        # auth_header = request.headers["Authorization"]
        # if not auth_header.startswith("Bearer "):
        #     raise HTTPException(status_code=401, detail="Invalid token format")
        # token = auth_header.split("Bearer ")[1]

        # # Verificar y decodificar el token
        # try:
        #     data = serializer.loads(token)
        #     print("Data", data)
        # except BadSignature:
        #     raise HTTPException(status_code=401, detail="Invalid token")
        # except SignatureExpired:
        #     raise HTTPException(status_code=401, detail="Token expired")

        # if request_count_path >= self.limit_per_path:
        #     return Response (f"Too Many Path Requests: {request_count_path}", status_code=429)

        self.db_service.log_request(remote_ip, request_path)
        response = await call_next(request)
        return response
