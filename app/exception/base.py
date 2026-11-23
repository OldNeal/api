from fastapi import HTTPException
from app.validate.core import BaseExceptionResponse
from app.validate.api.base import CoreErrorResponse
from app.logging.base import log

class BaseException(HTTPException):
    status_code = 500
    default_message = 'The base exception'
    model_response: type[BaseExceptionResponse] = BaseExceptionResponse

    def __init__(self, message: str | None = None, to_print: bool = True, **kwargs):
        super().__init__(status_code=self.status_code, detail=message or self.default_message)
        self.headers = self.headers
        self.kwargs = kwargs
        self.details = self.detail.format_map(kwargs)
        self.message = self.template.format(name=self.name, status_code=self.status_code, details=self.details)
        self.content = self.model_dump()
        if to_print:
            log.warning(self.message, **kwargs)

    @property
    def template(self):
        return "❌ {name} [{status_code}]: {details}"

    @property
    def name(self):
        return self.__class__.__name__

    @classmethod
    def type(self):
        return self.__module__.replace('app.exception.', '').removesuffix('.py')

    def model_dump(self, **kwargs):
        return self.model_response.model_validate(self.__dict__ | {'type':self.type()} | kwargs).model_dump()

class PermissionException(BaseException):
    default_message = 'Нет доступа'    
    status_code = 403

class ParametrValidationException(BaseException):
    default_message = 'Ошибка валидации query или path аргументов в endpoints'    
    status_code = 422

class TokenDontFind(BaseException):
    default_message = 'Токен не найден'    
    status_code = 432

class RedisError(BaseException):
    default_message = 'Redis не работает'

class CoreError(BaseException):
    default_message = 'Ошибка в Core'
    status_code = 400
    model_response: type[CoreErrorResponse] = CoreErrorResponse

    @property
    def template(self):
        return "❌ {name} [{status_code}]: {details}"
    
    @property
    def code(self):
        return self.kwargs.get('status_code')

    @property
    def original_exception(self):
        return self.kwargs.get('original_exception')

    def model_dump(self, **kwargs):
        return super().model_dump(**kwargs | {'original_exception':self.original_exception})

class CoreTimeoutError(BaseException):
    default_message = 'Core не работает'

class PageDontFindError(BaseException):
    default_message = 'Станица не найдена'
    status_code = 475