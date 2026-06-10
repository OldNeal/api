from app.validate.api.base import QueryBody
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class UserMidlware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.json()
        query_body = QueryBody(**body)
        response = await call_next(request)
        return response

