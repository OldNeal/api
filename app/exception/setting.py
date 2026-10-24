from app.exception.base import BaseException

class SettingException(BaseException):
    default_message = 'The setting exception'

class ParametrValidateError(SettingException):
    default_message = 'Неправильный тип данных в параметре {parametr_tag}. Значение этого параметра может быть только {parametr_type}'
    status_code = 470

class RankValidateError(SettingException):
    default_message = 'В параметре {parametr_tag} нужно указать существующий ранг. Максимальный ранг - {max_rank}, минимальный - {min_rank}'
    status_code = 470

class ParametrExistError(SettingException):
    default_message = 'Несуществующий параметр {parametr_tag}. Проверьте есть ли такой параметр и нету ли опечаток в параметре'
    status_code = 470