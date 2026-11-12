from app.exception.base import BaseException

class ActivityPointLimitError(BaseException):
    default_message = 'Вы исчерпали лимит очков активности в час'
    status_code = 480