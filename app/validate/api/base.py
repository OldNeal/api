from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime, timedelta
from typing import Literal, Any

from app.validate.core import BaseExceptionResponse

class BaseAPIValidate(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class QueryBody(BaseAPIValidate):
    token: str
    is_admin: bool = False

class CoreErrorResponse(BaseExceptionResponse):
    original_exception: BaseExceptionResponse