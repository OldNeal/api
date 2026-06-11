from app.db.dao.base import BaseDAO, AsyncSession
from app.db.models.main import ChatDB, UserDB, TgChatDB, TgUserDB
from app.db.models.beyonder import BeyonderDB, PathDB, SequenceDB, GreatAncientDB
from app.db.models.organ import OrganDB, MemberDB, OrganPermissionDB
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete, func, join, or_, all_, and_, any_
from sqlalchemy.orm import selectinload, joinedload
from app.db.base import Base
from datetime import datetime, date

class UserDAO(BaseDAO[UserDB]):
    model = UserDB

    async def query_by_tg_id(self, tg_id: int):
        return await self.find_one_or_none({'tg_id':tg_id})

class ChatDAO(BaseDAO[ChatDB]):
    model = ChatDB
    
    async def query_by_tg_id(self, tg_id: int):
        return await self.find_one_or_none({'tg_id':tg_id})

class TgChatDAO(BaseDAO[TgChatDB]):
    model = TgChatDB

    async def query_by_tg_id(self, tg_id: int):
        return await self.find_one_or_none({'tg_id':tg_id})

class TgUserDAO(BaseDAO[TgUserDB]):
    model = TgUserDB

    async def query_by_tg_id(self, tg_id: int):
        return await self.find_one_or_none({'tg_id':tg_id})

class BeyonderDAO(BaseDAO[BeyonderDB]):
    model = BeyonderDB
    
    async def query_by_user_id(self, user_id: int):
        return await self.find_one_or_none({'user_id':user_id})

class PathDAO(BaseDAO[PathDB]):
    model = PathDB
    load = [model.sequence_datas]

    async def query_by_group(self, group: str):
        try:
            query = select(self.model).join(GreatAncientDB).filter_by(group=group).options(selectinload(self.model.sequence_datas))
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def query_by_name(self, name: str):
        try:
            query = select(self.model).join(SequenceDB).where(SequenceDB.name.ilike(name)).options(selectinload(self.model.sequence_datas))
            result = await self.session.execute(query)
            record = result.scalars().first()
            return record
        except SQLAlchemyError as e:
            raise

    async def search_by_name(self, name: str):
        try:
            query = select(self.model).join(SequenceDB).where(or_(*[func.lower(SequenceDB.name).contains(f'%{n}%') for n in name.split(' ')])).options(selectinload(self.model.sequence_datas))
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

class SequenceDAO(BaseDAO[SequenceDB]):
    model = SequenceDB

    async def query_by_name(self, name: str):
        return await self.find_one_or_none({'name':name})

class GreatAncientDAO(BaseDAO[GreatAncientDB]):
    model = GreatAncientDB

    async def query_by_name(self, name: str):
        return await self.find_one_or_none({'name':name})

    async def query_by_name(self, name: str):
        try:
            query = select(self.model).where(self.model.name.ilike(name)).options(selectinload(self.model.paths).selectinload(PathDB.sequence_datas))
            result = await self.session.execute(query)
            record = result.scalars().first()
            return record
        except SQLAlchemyError as e:
            raise

    async def search_by_name(self, name: str):
        try:
            query = select(self.model).where(or_(*[func.lower(self.model.name).contains(f'%{n}%') for n in name.split(' ')])).options(selectinload(self.model.paths).selectinload(PathDB.sequence_datas))
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

class OrganDAO(BaseDAO[OrganDB]):
    model = OrganDB

    async def query_by_name(self, name: str):
        return await self.find_one_or_none({'name':name})

class MemberDAO(BaseDAO[MemberDB]):
    model = MemberDB

    async def query_by_user_id(self, user_id: int):
        return await self.find_one_or_none({'user_id':user_id})

class OrganPermissionDAO(BaseDAO[OrganPermissionDB]):
    model = OrganPermissionDB

class DAO:
    def __init__(self, session: AsyncSession):
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
    