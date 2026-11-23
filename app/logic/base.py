from datetime import datetime

from app.core import client, schemas, config
from app.logging.base import botlog
from app.exception.base import CoreTimeoutError, TokenDontFind
from app.logic.utils import class_decor, BaseExceptionResponse
from app.redis.store import store

@class_decor
class BaseLogic:
    client = client
    schemas = schemas
    store = store

    def __init__(self, token: str | None = None, **kwargs):
        self.token = token
        self.kwargs = kwargs
        self.client.client.config.headers =  self.client.client.config.headers | {
            'request_id':self.request_id, 
            'platform':'api'
            }
        self.client.client.config.timeout = 10

    @property
    async def user_id(self):
        if self.token:
            return await self.get_user_id(self.token) 
        raise TokenDontFind()

    @property
    async def body(self):
        return self.schemas.QueryBody(
            user_id=await self.user_id, 
            is_admin=self.is_admin
            )

    async def get_user_id(self, token: str):
        user_id = await self.store.user.get_user_id(token)
        if user_id is None:
            raise TokenDontFind()
        return user_id

    @property
    def is_admin(self):
        return self.kwargs.get('is_admin', False)

    @property
    def request_id(self):
        return self.kwargs.get('request_id')
        
    @classmethod
    async def test_core_connect(cls, logged: bool = True, is_raise: bool = False):
        try:
            start = datetime.now()
            cls.client.client.config.headers = {
                'platform':'api'
                }
            cls.client.client.config.timeout = 10
            response = await cls.client.main()
            if response:
                end = datetime.now()
                result = f'{int((end - start).total_seconds()*1000)}'
                if logged:
                    botlog.logger.info('Core работает', ping=result, url=cls.client.client.config.base_url)
                return response
        except Exception as e:
            exc = CoreTimeoutError(url=cls.client.client.config.base_url)
            if is_raise:
                raise exc

    def redact_kwargs(self, **new_kwargs):
        self.kwargs |= new_kwargs
        return self

    def check_is_not_none(self, *objs):
        for obj in objs:
            if not obj is None:
                return obj