from app.exception.base import BaseException

class OrganException(BaseException):
    default_message = 'The organ exception'

class DontMemberError(OrganException):
    default_message = 'Пользователь не участник организации'
    status_code = 458

class ALreadyMemberError(OrganException):
    default_message = 'Пользователь уже участник организации'
    status_code = 459

class OrganPermissioError(BaseException):
    default_message = 'Нет доступа'    
    status_code = 460

class OrganPermissionNewRankError(BaseException):
    default_message = 'Нет доступа, новый ранг выше или равен вашему'    
    status_code = 461

class OrganPermissionPurposeRankError(BaseException):
    default_message = 'Нет доступа, ранг участника выше или равен вашему'    
    status_code = 462

class InOneOrganError(OrganException):
    default_message = 'Пользователь не участник вашей организации'
    status_code = 463

class ExistOrganError(OrganException):
    default_message = 'Организация не найдена'
    status_code = 464

class HiddenOrganError(OrganException):
    default_message = 'Информация о организации скрыта'
    status_code = 465

class ClosenOrganError(OrganException):
    default_message = 'Организация не принимает участников'
    status_code = 466
    
class ExistRankError(OrganException):
    default_message = 'Такого ранга нету'
    status_code = 467

class ALreadyOwnerError(OrganException):
    default_message = 'Вы уже глава организации'
    status_code = 468
    
class DontEnterPurposeError(OrganException):
    default_message = 'Вы не указали участника'
    status_code = 469