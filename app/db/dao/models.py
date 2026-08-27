from app.db.dao.base import BaseDAO, AsyncSession
from app.db.models.main import ChatDB, UserDB, TgChatDB, TgUserDB
from app.db.models.beyonder import BeyonderDB, PathDB, SequenceDB, GreatAncientDB
from app.db.models.organ import OrganDB, MemberDB
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete, func, join, or_, all_, and_, any_
from sqlalchemy.orm import selectinload, joinedload
from app.db.base import Base
from datetime import datetime, date

class UserDAO(BaseDAO[UserDB]):
    model = UserDB

    async def query_by_tg_id(self, tg_id: int):
        return await self.find_one_or_none({'tg_id':tg_id})

    async def get_organ_owner_by_organ_id(self, organ_id: int):
        try:
            query = select(self.model).join(MemberDB).filter_by(organ_id=organ_id, rank=0)
            result = await self.session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise

    async def get_members_by_organ_id(self, organ_id: int):
        try:
            query = select(self.model).join(MemberDB).filter_by(organ_id=organ_id)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise


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
    load = [selectinload(model.sequence_datas)]

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
            query = select(self.model).join(SequenceDB).where(or_(*[func.lower(SequenceDB.name).contains(f'%{n}%') for n in name.lower().split(' ')])).options(selectinload(self.model.sequence_datas))
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def query_many_by_ga_id(self, ga_id: int):
        return await self.find_all({'ga_id':ga_id})

class SequenceDAO(BaseDAO[SequenceDB]):
    model = SequenceDB

    async def query_by_name(self, name: str):
        return await self.find_one_or_none({'name':name})

    async def query_by_path_id(self, path_id: int, number: int):
        return await self.find_one_or_none({'path_id':path_id, 'number':number})

    async def query_many_by_path_id(self, path_id: int):
        return await self.find_all({'path_id':path_id})


class GreatAncientDAO(BaseDAO[GreatAncientDB]):
    model = GreatAncientDB
    load = [selectinload(model.paths).selectinload(PathDB.sequence_datas)]

    async def search_by_name(self, name: str):
        try:
            query = select(self.model).where(or_(*[func.lower(self.model.name).contains(f'%{n}%') for n in name.split(' ')])).options(selectinload(self.model.paths).selectinload(PathDB.sequence_datas))
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def gropus(self):
        try:
            query = select(self.model.group)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return list(set(record))
        except SQLAlchemyError as e:
            raise


class OrganDAO(BaseDAO[OrganDB]):
    model = OrganDB
    load = [selectinload(model.members)]

    async def query_by_name(self, name: str):
        return await self.find_one_or_none({'name':name})

    async def get_members_count(self, organ_id: int):
        """Получить количество участников в организации"""
        try:
            query = select(self.model).filter_by(id=organ_id)
            result = await self.session.execute(query)
            record = result.scalars().all().count()
            return record
        except SQLAlchemyError as e:
            raise

    async def search_by_name(self, name: str):
        try:
            query = select(self.model).where(or_(*[func.lower(self.model.name).contains(f'%{n}%') for n in name.lower().split(' ')]))
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

class MemberDAO(BaseDAO[MemberDB]):
    model = MemberDB

    async def query_by_user_id(self, user_id: int):
        return await self.find_one_or_none({'user_id':user_id})

    async def get_owner(self, organ_id: int):
        return await self.find_one_or_none({'organ_id':organ_id, 'rank':0})

    async def get_members(self, organ_id: int):
        return await self.find_all({'organ_id':organ_id})
    
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

    async def flush(self):
        await self.session.flush()  

    async def commit(self):
        await self.session.commit()    

    async def close(self):
        await self.session.close()        
        
    async def rollback(self):
        await self.session.rollback()  
