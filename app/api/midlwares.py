from fastapi import Request
from json import JSONDecodeError
from starlette.middleware.base import BaseHTTPMiddleware
from app.validate.api.base import QueryBody
from app.logging.base import botlog
import uuid

class LogMidlware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get('request_id', uuid.uuid4().hex)
        platform = request.headers.get('platform')
        context = {'platform':platform, 'client_ip':request.client.host, 'request_id':request_id}
        try:
            payload = await request.json()
            body = QueryBody(**payload)
            context = {'user_id':body.user_id} | context | {'is_admin':body.is_admin}
            telegram = payload.get('telegram')
            tg_id = telegram.get('tg_id') if isinstance(telegram, dict) else None
            if tg_id is not None:
                context |= {'tg_id':tg_id}
        except JSONDecodeError:
            pass
        with botlog.logger.contextualize(**context):
            with botlog.logger.catch(reraise=True):
                response = await call_next(request)
                botlog.query(request.url, request.method, status_code=response.status_code)
                return response
