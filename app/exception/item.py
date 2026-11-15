from app.exception.base import BaseException


class ItemDontFindException(BaseException):
    default_message = 'Предмет не найден'
    status_code = 437


class ItemQuantityException(BaseException):
    default_message = 'Недостаточно предметов: запрошено {quantity}, доступно {available}'
    status_code = 438
