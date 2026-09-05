from fastapi import Request
from json import JSONDecodeError
from starlette.middleware.base import BaseHTTPMiddleware
from app.validate.api.base import QueryBody
from app.db.metods.check import check_user
from app.logging.base import botlog
import uuid

class UpdateUserInfoMidlware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = None
        context = {'client_ip':request.client.host, 'request_id':uuid.uuid4().hex}
        try:
            body = await request.json()
            body = QueryBody(**body)
            if body.enter_body:
                user = await check_user(**body.model_dump())
            if body.chat_id:
                context = {'chat_id':body.chat_id} | context
            if body.request_id:
                context |= {'request_id':body.request_id}
            context = {'tg_id':body.tg_id} | context
        except JSONDecodeError:
            pass
        with botlog.logger.contextualize(**context):
            with botlog.logger.catch(reraise=True):
                response = await call_next(request)
                botlog.query(request.url, request.method, status_code=response.status_code)
                return response

