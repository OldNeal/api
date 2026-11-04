from app.exception.base import BaseException


class QuestionDontFindException(BaseException):
    default_message = 'Вопрос не найден'
    status_code = 435


class AnswerDontFindException(BaseException):
    default_message = 'Ответ не найден в указанном вопросе'
    status_code = 436
