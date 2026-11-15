from app.exception.base import BaseException

class ActivityPointLimitError(BaseException):
    default_message = 'Вы исчерпали лимит очков активности'
    status_code = 480