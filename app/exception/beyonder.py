from app.exception.base import BaseException

class BeyonderException(BaseException):
    default_message = 'The beyonder exception'

class DontBeyonderException(BaseException):
    default_message = 'Пользователь не потусторонний'
    status_code = 453

class ALreadyBeyonderException(BaseException):
    default_message = 'Пользователь уже потусторонний'
    status_code = 454

class UpseqNotComeException(BaseException):
    default_message = 'Зелье еще не переварилось, осталось дней: {upseq_days}'
    status_code = 455

    @property
    def template(self):
        return "⌛ {details}"

class SeqDontExistException(BaseException):
    default_message = 'Незвестная последовательность'
    status_code = 456

class PathDontEnterException(BaseException):
    default_message = 'Путь не указан'
    status_code = 457




    