from app.exception.base import BaseException
from config import MAX_DAILY_QUESTION_ANSWERS


class QuestionDontFindException(BaseException):
    default_message = 'Вопрос не найден'
    status_code = 435


class AnswerDontFindException(BaseException):
    default_message = 'Ответ не найден в указанном вопросе'
    status_code = 436


class QuestionAlreadyAnsweredException(BaseException):
    default_message = 'Повторно ответить на этот вариант можно только через 2 недели после предыдущего ответа'
    status_code = 409


class QuestionDailyLimitException(BaseException):
    default_message = (
        f'Достигнут дневной лимит: можно ответить максимум на '
        f'{MAX_DAILY_QUESTION_ANSWERS} вопросов в день'
    )
    status_code = 429
