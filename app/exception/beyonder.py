from datetime import timedelta
from math import ceil

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
    status_code = 455

    def __init__(self, remaining_time: timedelta, **kwargs):
        if remaining_time.days > 1:
            message = f'Зелье еще не переварилось, осталось дней: {remaining_time.days}'
        else:
            total_seconds = max(0, ceil(remaining_time.total_seconds()))
            hours, seconds = divmod(total_seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            time_text = ''
            if hours > 0:
                time_text += f'{hours} ч. '
            if minutes > 0:
                time_text += f'{minutes} мин. '
            if seconds > 0:
                time_text += f'{seconds} сек. '
            message = 'Зелье еще не переварилось, осталось: ' + time_text
        super().__init__(message=message, **kwargs)

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



    