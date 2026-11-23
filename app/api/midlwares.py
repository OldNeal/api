from fastapi import Request
from json import JSONDecodeError
from starlette.middleware.base import BaseHTTPMiddleware
from app.validate.api.base import QueryBody
from app.logging.base import botlog
import uuid

class LogMidlware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = uuid.uuid4().hex
        context = {'client_ip':request.client.host, 'request_id':request_id}
        request.state.request_id = request_id
        try:
            payload = await request.json()
            body = QueryBody(**payload)
            context = {'token':body.token} | context | {'is_admin':body.is_admin}
        except JSONDecodeError:
            pass
        with botlog.logger.contextualize(**context):
            with botlog.logger.catch(reraise=True):
                response = await call_next(request)
                botlog.query(request.url, request.method, status_code=response.status_code)
                return response
