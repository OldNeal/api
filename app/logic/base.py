from app.db.dao.models import DAO
from app.exception.base import PermissionException, UserDontFind
from app.exception.beyonder import DontBeyonderException
from app.validate.api.base import TelegramBody, AnswerUserBody
from app.logging.base import botlog

class BaseLogic:
    def __init__(self, session, user_id: int | None = None, purpose_user_id: int | None = None, is_admin: bool = False):
        self.dao = DAO(session)
        self.user_id = user_id
        self.purpose_user_id = purpose_user_id or user_id
        self.is_admin = is_admin
        self.botlog = botlog.bind(purpose_user_id=purpose_user_id)
        self.log_kwargs = {}
    
    def check_is_not_none(self, *objs):
        for obj in objs:
            if not obj is None:
                return obj

    async def get_user(self, purpose_user_id: int | None = None, is_raise_not_beyonder: bool = False, only_user: bool = False):
        user = await self.dao.user.query_by_user_id(
            self.check_is_not_none(purpose_user_id, self.purpose_user_id, self.user_id)
            if not only_user
            else self.user_id
        )
        if user:
            if user.beyonder:
                await user.beyonder.seq.path.awaitable_attrs.sequence_datas
                await user.beyonder.awaitable_attrs.ga
            elif is_raise_not_beyonder:
                raise DontBeyonderException(purpose_user_id=self.purpose_user_id)
        else:
            raise UserDontFind()
        return user
    
    def check_permission(self, is_admin_value: bool = True):
        if self.is_admin != is_admin_value:
            raise PermissionException()
        return self.is_admin
    
    async def query_body(self, user_id: int | None = None):
        user = await self.get_user(user_id)
        return self.return_query_body(user)
        
    def return_query_body(self, user):
        return AnswerUserBody(
            user_id=user.id,
            name=user.name,
            telegram=TelegramBody(
                tg_id=user.tg_id,
                username=user.tg_user.username,
                fullname=user.tg_user.fullname,
            ) if user.tg_user else None
        )
    
