from app.exception.base import BaseException

class BeyonderException(BaseException):
    default_message = 'The beyonder exception'

class DontBeyonderException(BeyonderException):
    default_message = 'Пользователь не потусторонний'
    status_code = 453

class ALreadyBeyonderException(BeyonderException):
    default_message = 'Пользователь уже потусторонний'
    status_code = 454

class UpseqNotComeException(BeyonderException):
    default_message = 'Зелье еще не переварилось, осталось дней: {upseq_days}'
    status_code = 455

    @property
    def template(self):
        return "⌛ {details}"

class SeqDontExistException(BeyonderException):
    default_message = 'Незвестная последовательность'
    status_code = 456

class PathDontEnterException(BeyonderException):
    default_message = 'Путь не указан'
    status_code = 457

class SeqBusyException(BeyonderException):
    default_message = 'Последовательность уже занята'
    status_code = 471



    