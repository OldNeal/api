from fastapi import HTTPException
from app.validate.api.exception import BaseExceptionResponse
from app.logging.base import log

class BaseException(HTTPException):
    status_code = 400
    default_message = 'The base exception'
    model_response: type[BaseExceptionResponse] = BaseExceptionResponse

    def __init__(self, message: str | None = None, **kwargs):
        super().__init__(status_code=self.status_code, detail=message or self.default_message, headers=kwargs)
        self.headers = self.headers
        self.details = self.detail.format_map(kwargs)
        self.message = self.template.format(name=self.name, status_code=self.status_code, details=self.details)
        self.content = self.model_response.model_validate(self.__dict__ | {'type':self.type()}).model_dump()
        log.warning(self.message)

    @property
    def template(self):
        return "❌ {name} [{status_code}]: {details}"

    @property
    def name(self):
        return self.__class__.__name__

    @classmethod
    def type(self):
        return self.__module__.replace('app.exception.', '')

class PermissionException(BaseException):
    default_message = 'Нет доступа'    
    status_code = 403

class ParametrValidationException(BaseException):
    default_message = 'Ошибка валидации query или path аргументов в endpoints'    
    status_code = 422

class UserDontFind(BaseException):
    default_message = 'Пользователь не найден'    
    status_code = 432
    