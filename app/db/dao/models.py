from app.db.dao.base import BaseDAO, AsyncSession
from app.db.models.main import ChatDB, UserDB, TgChatDB, TgUserDB
from app.db.models.beyonder import BeyonderDB, PathDB, SequenceDB, GreatAncientDB
from app.db.models.organ import OrganDB, MemberDB
from app.db.models.newspaper import NewsPaperDB, ReaderDB, EDITOR_RANK
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete, func, join, or_, all_, and_, any_
from sqlalchemy.orm import selectinload, joinedload
from app.db.base import Base
from datetime import datetime, date

class UserDAO(BaseDAO[UserDB]):
    model = UserDB
    load = [joinedload(model.beyonder).joinedload(BeyonderDB.seq).joinedload(SequenceDB.path).joinedload(PathDB.god)]

    def _search_users_query(
        self,
        user_id: int | None = None,
        tg_id: int | None = None,
        username: str | None = None,
        name: str | None = None,
    ):
        filters = []
        if user_id is not None:
            filters.append(self.model.id == user_id)
        elif tg_id is not None:
            filters.append(self.model.tg_id == tg_id)
        elif username and username.strip().lstrip('@'):
            filters.append(
                func.lower(TgUserDB.username).contains(
                    username.strip().lstrip('@').lower(),
                    autoescape=True,
                )
            )
        elif name and name.strip():
            filters.append(
                func.lower(func.coalesce(self.model._name, TgUserDB.fullname)).contains(
                    name.strip().lower(),
                    autoescape=True,
                )
            )

        query = (
            select(self.model)
            .outerjoin(TgUserDB, TgUserDB.tg_id == self.model.tg_id)
            .order_by(
                func.lower(
                    func.coalesce(TgUserDB.fullname, TgUserDB.username, self.model._name, '')
                ),
                self.model.id,
            )
        )
        if filters:
            query = query.where(or_(*filters))
        if self.load:
            query = query.options(*self.load)
        return query

    async def search_users_paginated(
        self,
        user_id: int | None = None,
        tg_id: int | None = None,
        username: str | None = None,
        name: str | None = None,
        page: int | None = None,
        per_page: int = 5,
    ):
        return await self.paginate(
            self._search_users_query(user_id, tg_id, username, name),
            page,
            per_page,
        )

    async def query_by_user_id(self, user_id: int):
        return await self.find_one_or_none({'id':user_id})

    async def query_by_tg_id(self, tg_id: int):
        return await self.find_one_or_none({'tg_id':tg_id})

    async def search_users(
        self,
        user_id: int | None = None,
        tg_id: int | None = None,
        username: str | None = None,
        name: str | None = None,
        page: int | None = None,
        per_page: int = 5,
    ):
        query = self._search_users_query(user_id, tg_id, username, name)
        if page is not None:
            query = query.offset(page * per_page).limit(per_page)
        result = await self.session.execute(query)
        return result.unique().scalars().all()

    async def get_all_users(
        self,
        page: int | None = None,
        per_page: int = 5,
        ):
        return await self.search_users(page=page, per_page=per_page)

    async def get_organ_owner_by_organ_id(self, organ_id: int):
        try:
            query = select(self.model).join(MemberDB).filter_by(organ_id=organ_id, rank=0)
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise

    async def get_members_by_organ_id(self, organ_id: int):
        try:
            query = select(self.model).join(MemberDB).filter_by(organ_id=organ_id)
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def get_members_by_organ_id_paginated(
        self,
        organ_id: int,
        page: int | None = None,
        per_page: int = 5,
    ):
        query = (
            select(self.model)
            .join(MemberDB)
            .where(MemberDB.organ_id == organ_id)
            .order_by(MemberDB.rank, self.model.id)
        )
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

    async def get_beyonders_by_path_id(self, path_id: int):
        try:
            query = select(self.model).join(BeyonderDB).join(SequenceDB).filter_by(path_id=path_id)
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def get_beyonders_by_path_id_paginated(
        self,
        path_id: int,
        page: int | None = None,
        per_page: int = 5,
    ):
        query = (
            select(self.model)
            .join(BeyonderDB)
            .join(SequenceDB)
            .where(SequenceDB.path_id == path_id, BeyonderDB.ga_id.is_(None))
            .order_by(SequenceDB.number, self.model.id)
        )
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

    async def get_ga_by_path_id(self, path_id: int):
        try:
            subquery = select(PathDB.ga_id).filter_by(id=path_id).scalar_subquery()
            query = select(self.model).join(BeyonderDB).filter_by(ga_id=subquery)
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalar_one_or_none()
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

    async def query_many_by_path_id(self, path_id: int):
        try:
            query = select(self.model).join(SequenceDB).filter_by(path_id=path_id)
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def query_by_path_id(self, path_id: int, seq: int):
        try:
            query = select(self.model).join(SequenceDB).filter_by(path_id=path_id, number=seq)
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def query_ga_by_ga_id(self, ga_id: int):
        try:
            query = select(self.model).filter_by(ga_id=ga_id)
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise

class PathDAO(BaseDAO[PathDB]):
    model = PathDB
    load = [selectinload(model.sequence_datas)]

    async def query_by_group(self, group: str):
        try:
            query = select(self.model).join(GreatAncientDB).filter_by(group=group)
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def query_by_name(self, name: str):
        try:
            query = select(self.model).join(SequenceDB).where(SequenceDB.name.ilike(name))
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().first()
            return record
        except SQLAlchemyError as e:
            raise

    async def search_by_name(self, name: str):
        try:
            query = select(self.model).join(SequenceDB).where(or_(*[func.lower(SequenceDB.name).contains(f'%{n}%') for n in name.lower().split(' ')]))
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def search_by_name_paginated(
        self,
        name: str,
        page: int | None = None,
        per_page: int = 5,
    ):
        query = (
            select(self.model)
            .join(SequenceDB)
            .where(or_(*[
                func.lower(SequenceDB.name).contains(f'%{term}%')
                for term in name.lower().split(' ')
            ]))
            .distinct()
            .order_by(self.model.id)
        )
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

    async def query_many_by_ga_id(self, ga_id: int):
        return await self.find_all({'ga_id':ga_id})

    async def query_many_by_ga_id_paginated(
        self,
        ga_id: int,
        page: int | None = None,
        per_page: int = 5,
    ):
        query = (
            select(self.model)
            .where(self.model.ga_id == ga_id)
            .order_by(self.model.id)
        )
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

class SequenceDAO(BaseDAO[SequenceDB]):
    model = SequenceDB

    async def query_by_name(self, name: str):
        return await self.find_one_or_none({'name':name})

    async def query_by_path_id(self, path_id: int, number: int):
        return await self.find_one_or_none({'path_id':path_id, 'number':number})

    async def query_many_by_path_id(self, path_id: int):
        return await self.find_all({'path_id':path_id})

    async def search_by_name_paginated(
        self,
        name: str,
        page: int | None = None,
        per_page: int = 5,
    ):
        terms = [term for term in name.casefold().split() if term]
        query = select(self.model)
        if terms:
            query = query.where(or_(*[
                func.lower(self.model.name).contains(term)
                for term in terms
            ]))
        query = query.order_by(self.model.path_id, self.model.number, self.model.id)
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

    async def query_many_by_path_id_paginated(
        self,
        path_id: int,
        page: int | None = None,
        per_page: int = 5,
    ):
        query = (
            select(self.model)
            .where(self.model.path_id == path_id)
            .order_by(self.model.number, self.model.id)
        )
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)


class GreatAncientDAO(BaseDAO[GreatAncientDB]):
    model = GreatAncientDB
    load = [selectinload(model.paths).selectinload(PathDB.sequence_datas)]

    async def get_by_group(self, group: str):
        query = select(self.model).where(self.model.group == group).order_by(self.model.id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def search_by_name(self, name: str):
        try:
            query = select(self.model).where(or_(*[func.lower(self.model.name).contains(f'%{n}%') for n in name.split(' ')]))
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def search_by_name_paginated(
        self,
        name: str,
        page: int | None = None,
        per_page: int = 5,
    ):
        query = select(self.model).where(or_(*[
            func.lower(self.model.name).contains(f'%{term}%')
            for term in name.split(' ')
        ])).order_by(self.model.id)
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

    async def gropus(self):
        try:
            query = select(self.model.group)
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return list(set(record))
        except SQLAlchemyError as e:
            raise

    async def groups_paginated(self, page: int | None = None, per_page: int = 5):
        query = select(self.model.group).distinct().order_by(self.model.group)
        count_query = select(func.count()).select_from(
            select(self.model.group).distinct().subquery()
        )
        count = await self.session.scalar(count_query) or 0
        if page is not None:
            query = query.offset(page * per_page).limit(per_page)
        result = await self.session.execute(query)
        return list(result.scalars().all()), count


class OrganDAO(BaseDAO[OrganDB]):
    model = OrganDB
    load = [selectinload(model.members)]

    async def search_by_name(self, name: str):
        try:
            query = select(self.model).where(or_(*[func.lower(self.model.name).contains(f'%{n}%') for n in name.lower().split(' ')]))
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def search_by_name_paginated(
        self,
        name: str,
        page: int | None = None,
        per_page: int = 5,
    ):
        query = (
            select(self.model)
            .where(or_(*[
                func.lower(self.model.name).contains(f'%{term}%')
                for term in name.lower().split(' ')
            ]))
            .order_by(self.model.id)
        )
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

    async def top_by_members_paginated(
        self,
        page: int | None = None,
        per_page: int = 5,
    ):
        top_organs = (
            select(
                self.model.id.label('id'),
                func.count(MemberDB.user_id).label('member_count'),
            )
            .outerjoin(MemberDB)
            .group_by(self.model.id)
            .order_by(func.count(MemberDB.user_id).desc(), self.model.id)
            .limit(6)
            .subquery()
        )
        query = (
            select(self.model)
            .join(top_organs, self.model.id == top_organs.c.id)
            .order_by(top_organs.c.member_count.desc(), self.model.id)
        )
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

    async def top_by_created_at_paginated(
        self,
        page: int | None = None,
        per_page: int = 5,
    ):
        top_organs = (
            select(self.model.id.label('id'), self.model.created_at.label('created_at'))
            .order_by(self.model.created_at, self.model.id)
            .limit(6)
            .subquery()
        )
        query = (
            select(self.model)
            .join(top_organs, self.model.id == top_organs.c.id)
            .order_by(top_organs.c.created_at, self.model.id)
        )
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

class MemberDAO(BaseDAO[MemberDB]):
    model = MemberDB

    async def query_by_user_id(self, user_id: int):
        return await self.find_one_or_none({'user_id':user_id})

    async def get_owner(self, organ_id: int):
        return await self.find_one_or_none({'organ_id':organ_id, 'rank':0})

    async def get_members(self, organ_id: int):
        return await self.find_all({'organ_id':organ_id})

class NewsPaperDAO(BaseDAO[NewsPaperDB]):
    model = NewsPaperDB
    load = [selectinload(model.readers), selectinload(model.readers).selectinload(ReaderDB.user)]

    async def search_by_name(self, name: str):
        try:
            query = select(self.model).where(or_(*[func.lower(self.model.name).contains(f'%{n}%') for n in name.lower().split(' ')]))
            if self.load and len(self.load) > 0:
                query = query.options(*self.load)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise

    async def search_by_name_paginated(
        self,
        name: str,
        page: int | None = None,
        per_page: int = 5,
    ):
        query = (
            select(self.model)
            .where(or_(*[
                func.lower(self.model.name).contains(f'%{term}%')
                for term in name.lower().split(' ')
            ]))
            .order_by(self.model.id)
        )
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

    async def get_for_user_paginated(
        self,
        user_id: int,
        page: int | None = None,
        per_page: int = 5,
        editors_only: bool = False,
    ):
        query = (
            select(self.model)
            .join(ReaderDB)
            .where(ReaderDB.user_id == user_id)
        )
        if editors_only:
            editor_rank = func.coalesce(
                self.model.setting['editor_rank'].as_integer(),
                EDITOR_RANK,
            )
            query = query.where(ReaderDB.rank <= editor_rank)
        query = query.order_by(self.model.id)
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

    async def get_for_subscribe_paginated(
        self,
        user_id: int,
        page: int | None = None,
        per_page: int = 5,
    ):
        subscribed = (
            select(ReaderDB.id)
            .where(
                ReaderDB.news_paper_id == self.model.id,
                ReaderDB.user_id == user_id,
                ReaderDB.user_id == user_id,
            )
            .exists()
        )
        query = select(self.model).where(~subscribed).order_by(self.model.id)
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

class ReaderDAO(BaseDAO[ReaderDB]):
    model = ReaderDB
    load = [selectinload(model.user)]

    async def query_by_user_id(self, user_id: int):
        return await self.find_one_or_none({'user_id':user_id})

    async def get_owner(self, organ_id: int):
        return await self.find_one_or_none({'news_paper_id':organ_id, 'rank':0})

    async def get_members(self, organ_id: int):
        return await self.find_all({'news_paper_id':organ_id})

    async def get_readers_by_paper_id_paginated(
        self,
        news_paper_id: int,
        page: int | None = None,
        per_page: int = 5,
    ):
        query = (
            select(self.model)
            .where(self.model.news_paper_id == news_paper_id)
            .order_by(self.model.rank, self.model.user_id)
        )
        if self.load:
            query = query.options(*self.load)
        return await self.paginate(query, page, per_page)

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
        self.news_paper = NewsPaperDAO(self.session)
        self.reader = ReaderDAO(self.session)

    async def flush(self):
        await self.session.flush()  

    async def commit(self):
        await self.session.commit()    

    async def close(self):
        await self.session.close()        
        
    async def rollback(self):
        await self.session.rollback()  
