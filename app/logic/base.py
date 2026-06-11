from app.db.dao.models import DAO

class BaseLogic:
    def __init__(self, session, tg_id: int | None = None, purpose_tg_id: int | None = None, is_admin: bool = False):
        self.dao = DAO(session)
        self.tg_id = tg_id
        self.purpose_tg_id = purpose_tg_id
        self.is_admin = is_admin

    async def get_user(self, tg_id: int | None = None, is_raise_not_beyonder: bool = False):
        user = await self.dao.user.query_by_tg_id(tg_id if tg_id else self.tg_id)
        if user.beyonder:
            await user.beyonder.seq.path.awaitable_attrs.sequence_datas
        elif is_raise_not_beyonder:
            raise
        return user
    
    def check_permission(self, is_admin_value: bool = True):
        if self.is_admin != is_admin_value:
            raise
        return self.is_admin


    

