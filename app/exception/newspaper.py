from app.exception.base import BaseException

class NewsPaperException(BaseException):
    default_message = 'The news paper exception'

class NewsPaperPermissioError(BaseException):
    default_message = 'Нет доступа'    
    status_code = 472

class ExistNewsPaperError(NewsPaperException):
    default_message = 'Газета не найдена'
    status_code = 473
    
class ReaderError(NewsPaperException):
    default_message = 'Вы не читатель этой газеты'
    status_code = 474

class AlreadyReaderError(NewsPaperException):
    default_message = 'Вы уже читатель этой газеты'
    status_code = 474