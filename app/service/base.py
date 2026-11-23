from config import admins
from app.logic.base import BaseLogic

class BaseService:
    admins = admins
    logic_cls: type[BaseLogic] = BaseLogic
    logic: BaseLogic
    
    def __init__(self, token: str | None = None, is_admin: bool = False, **kwargs):
        self.token = token
        self.is_admin = token in self.admins and is_admin
        self.kwargs = kwargs
        self.logic = self.logic_cls(token, is_admin=is_admin, request_id=self.request_id)

    @property
    def request_id(self):
        return self.kwargs.get('request_id')
