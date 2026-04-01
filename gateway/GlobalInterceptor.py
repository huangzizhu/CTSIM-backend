from fastapi.responses import JSONResponse
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import json
import time

class GlobalInterceptor(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if 1 != 1:
            return JSONResponse(
                status_code=401, content={
                    "code": 0,
                    "message": "Unauthorized",
                    "data": None
                })
        endpoint = request.scope.get("endpoint")  # 当前请求对应的函数
        shouldLog = getattr(endpoint, "_enable_logging", False)
        if shouldLog:
            start_time = time.time()
            ip = request.client.host if request.client else None
            path = request.url.path
            method = request.method
            try:
                body = await request.json()
            except Exception:
                body = None
            # 放进 state
            log_data = {
                "ip": ip,
                "requestPath": path,
                "httpMethod": method,
                "body": body
            }
            print(log_data)
            response = await call_next(request)

        else:
            response = await call_next(request)
        return response