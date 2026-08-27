from app.exception.base import BaseException

class WikiException(BaseException):
    default_message = 'The wiki exception'
    
class PathDontSearchException(BaseException):
    default_message = 'Путь не найден'
    status_code = 433

class PathDontEnterFilterException(BaseException):
    default_message = 'Вы не указали ни имя, ни ID'
    status_code = 434

