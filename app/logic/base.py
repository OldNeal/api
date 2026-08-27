from app.db.dao.models import DAO
from app.exception.base import PermissionException, UserDontFind
from app.exception.beyonder import DontBeyonderException
from app.validate.api.base import QueryBody

class BaseLogic:
    def __init__(self, session, tg_id: int | None = None, purpose_tg_id: int | None = None, is_admin: bool = False):
        self.dao = DAO(session)
        self.tg_id = tg_id
        self.purpose_tg_id = purpose_tg_id or tg_id
        self.is_admin = is_admin

    def check_is_not_none(self, *objs):
        for obj in objs:
            if not obj is None:
                return obj

    async def get_user(self, purpose_tg_id: int | None = None, is_raise_not_beyonder: bool = False, only_user: bool = False):
        user = await self.dao.user.query_by_tg_id(self.check_is_not_none(purpose_tg_id, self.purpose_tg_id, self.tg_id) if not only_user else self.tg_id)
        if user:
            if user.beyonder:
                await user.beyonder.seq.path.awaitable_attrs.sequence_datas
                await user.beyonder.awaitable_attrs.ga
            elif is_raise_not_beyonder:
                raise DontBeyonderException(purpose_tg_id=self.purpose_tg_id)
        else:
            raise UserDontFind()
        return user
    
    def check_permission(self, is_admin_value: bool = True):
        if self.is_admin != is_admin_value:
            raise PermissionException()
        return self.is_admin
    
    async def query_body(self, tg_id: int | None = None):
        user = await self.get_user(tg_id)
        return self.return_query_body(user)
        
    def return_query_body(self, user):
        return QueryBody(tg_id=user.tg_id, username=user.tg_user.username, fullname=user.name, is_admin=self.is_admin)
    

