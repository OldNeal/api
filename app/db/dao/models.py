from app.db.dao.base import BaseDAO, AsyncSession
from app.db.models.main import ChatDB, UserDB, TgChatDB, TgUserDB
from app.db.models.beyonder import BeyonderDB, PathDB, SequenceDB, GreatAncientDB
from app.db.models.organ import OrganDB, MemberDB, OrganPermissionDB

class UserDAO(BaseDAO):
    model = UserDB

    async def query_by_tg_id(self, tg_id: int) -> UserDB | None:
        return await self.find_one_or_none({'tg_id':tg_id})

class ChatDAO(BaseDAO):
    model = ChatDB
    
    async def query_by_tg_id(self, tg_id: int) -> ChatDB | None:
        return await self.find_one_or_none({'tg_id':tg_id})

class TgChatDAO(BaseDAO):
    model = TgChatDB

    async def query_by_tg_id(self, tg_id: int) -> TgChatDB | None:
        return await self.find_one_or_none({'tg_id':tg_id})

class TgUserDAO(BaseDAO):
    model = TgUserDB

    async def query_by_tg_id(self, tg_id: int) -> TgUserDB | None:
        return await self.find_one_or_none({'tg_id':tg_id})

class BeyonderDAO(BaseDAO):
    model = BeyonderDB
    
    async def query_by_user_id(self, user_id: int) -> BeyonderDB | None:
        return await self.find_one_or_none({'user_id':user_id})

class PathDAO(BaseDAO):
    model = PathDB
    
class SequenceDAO(BaseDAO):
    model = SequenceDB

class GreatAncientDAO(BaseDAO):
    model = GreatAncientDB

class OrganDAO(BaseDAO):
    model = OrganDB

class MemberDAO(BaseDAO):
    model = MemberDB

    async def query_by_user_id(self, user_id: int) -> MemberDB | None:
        return await self.find_one_or_none({'user_id':user_id})

class OrganPermissionDAO(BaseDAO):
    model = OrganPermissionDB

class DAO:
    def __init__(self, session: AsyncSession):
        print(type(session))
        if type(session) != AsyncSession:
            raise TypeError('This session is not AsyncSession')
        self.session = session
        self.user = UserDAO(self.session)
        self.chat = ChatDAO(self.session)
        self.tgchat = TgChatDAO(self.session)
        self.tguser = TgUserDAO(self.session)
        self.beyonder = BeyonderDAO(self.session)
        self.path = PathDAO(self.session)
        self.sequence = SequenceDAO(self.session)
        self.greatancient = GreatAncientDAO(self.session)
        self.organ = OrganDAO(self.session)
        self.member = MemberDAO(self.session)
        self.organpermission = OrganPermissionDAO(self.session)

    async def add_or_update(self, tg_id: int):
        user = await self.user.query_by_tg_id(tg_id)
        return
    
