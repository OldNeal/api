from fastapi import Request
from json import JSONDecodeError
from starlette.middleware.base import BaseHTTPMiddleware
from app.validate.api.base import QueryBody
from app.db.metods.check import check_user

class UpdateUserInfoMidlware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = None
        try:
            body = await request.json()
            body = QueryBody(**body)
            if body.enter_body:
                await check_user(**body.model_dump())
        except JSONDecodeError:
            pass
        response = await call_next(request)
        return response

