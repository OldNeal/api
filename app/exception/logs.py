from app.exception.base import BaseException

class LogsFilesException(BaseException):
    status_code = 472

class DontExistCategoryException(LogsFilesException):
    default_message = 'Нет такой категории'

class DontHavePermissionException(LogsFilesException):
    default_message = 'Нет доступа'
    status_code = 403

class DontLogFileException(LogsFilesException):
    default_message = 'Только .log файлы'
