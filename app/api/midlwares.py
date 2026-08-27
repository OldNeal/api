from fastapi import Request
from json import JSONDecodeError
from starlette.middleware.base import BaseHTTPMiddleware
from app.validate.api.base import QueryBody
from app.db.metods.check import check_user
from app.logging.base import botlog

class UpdateUserInfoMidlware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = None
        context = {}
        try:
            body = await request.json()
            body = QueryBody(**body)
            if body.enter_body:
                user = await check_user(**body.model_dump())
            context |= {'tg_id':body.tg_id}
        except JSONDecodeError:
            pass
        with botlog.logger.contextualize(**context):
            with botlog.logger.catch(reraise=True):
                botlog.query(request.url, request.method)
                response = await call_next(request)
                return response

