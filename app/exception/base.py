from fastapi import HTTPException
from app.validate.api.exception import BaseExceptionResponse

class BaseException(HTTPException):
    status_code = 400
    default_message = 'The base exception'
    model_response: type[BaseExceptionResponse] = BaseExceptionResponse

    def __init__(self, message: str | None = None, **kwargs):
        super().__init__(status_code=self.status_code, detail=message or self.default_message, headers=kwargs)
        self.headers = self.headers
        self.message = self.detail
        self.content = self.model_response.model_validate(self.__dict__ | {'type':self.type()}).model_dump()

    def __str__(self) -> str:
        return f"{self.status_code}: {self.detail}"

    @classmethod
    def type(self):
        return self.__module__.replace('app.exception.', '')

class PermissionException(BaseException):
    default_message = 'Нет доступа'    
    status_code = 403

class ParametrValidationException(BaseException):
    default_message = 'Ошибка валидации query или path аргументов в endpoints'    
    status_code = 422