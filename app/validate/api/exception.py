from app.validate.api.base import datetime, Literal, BaseAPIValidate, Any


class BaseExceptionResponse(BaseAPIValidate):
    message: str
    status_code: int
    headers: dict | None = None
    content: Any = None


