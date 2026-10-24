from app.logic.base import BaseLogic
from app.validate.api.newspaper import (
    AnswerAllNewsPaperInfo,
    AnswerNewsPaperInfo,
    AnswerNewsPaperInfoReaders,
    AnswerNewsPaperInfoDescription,
    AnswerReaderInfo,
    AnswerRedactRank,
    AnswerNewsPaperGive,
    NewsPaperInfo,
    ForButtons
)
from app.validate.api.base import ReaderInfo
from app.db.models.newspaper import NewsPaperDB, ReaderDB, EDITOR_RANK, READER_RANK, AUTHOR_RANK
from app.db.models.main import UserDB
from app.exception.newspaper import ExistNewsPaperError, AlreadyReaderError, NewsPaperPermissioError, ReaderError
from app.logic.setting.base import NewsPaperSetting
from app.validate.api.organ import OrganSettingDefault
from app.validate.api.newspaper import AnswerNewsPaperSetting, AnswerNewsPaperSettingValues

class NewsPaperLogic(BaseLogic):
    def __init__(
        self,
        session,
        tg_id: int | None = None,
        purpose_tg_id: int | None = None,
        is_admin: bool = False,
        news_paper_id: int | None = None,
    ):
        super().__init__(session, tg_id, purpose_tg_id, is_admin)
        self.news_paper_id = news_paper_id

    async def check_reader(self, purpose_tg_id: int, news_paper_id: int, is_check_reader: bool = True):
        user = await self.get_user(purpose_tg_id)
        await user.awaitable_attrs.readers
        is_reader = news_paper_id in user.readers_by_news_paper_id
        if is_reader and not is_check_reader:
            raise AlreadyReaderError()
        if not is_reader and is_check_reader:
            raise ReaderError()
        return user

    async def check_exist_news_paper(self, news_paper_id: int):
        news_paper = await self.dao.news_paper.query_by_id(news_paper_id)
        if news_paper is None:
            raise ExistNewsPaperError()
        return news_paper

    async def check_permission(self, news_paper_id: int, permission_rank: int | None = None, setting_parametr: str | None = None):
        user = await self.check_reader(self.tg_id, news_paper_id)
        await user.awaitable_attrs.readers
        news_paper = user.news_papers.get(news_paper_id)
        reader = user.readers_by_news_paper_id.get(news_paper_id)
        if reader and (permission_rank is not None or setting_parametr is not None):
            if permission_rank is None and setting_parametr:
                permission_rank = NewsPaperSetting(news_paper.setting).values.get(setting_parametr)
            if permission_rank is None or reader.rank > permission_rank:
                raise NewsPaperPermissioError()
        return user, news_paper

    async def return_reader_info(self, reader: ReaderDB, for_buttons: ForButtons | None = None):
        user = await reader.awaitable_attrs.user
        news_paper = await reader.awaitable_attrs.news_paper
        return AnswerReaderInfo(
            user=self.return_query_body(user),
            reader=ReaderInfo(
                news_paper_name=news_paper.name,
                news_paper_id=news_paper.id,
                rank=reader.rank,
                rank_name=reader.rank_name,
            ),
            for_buttons=for_buttons
        ) if user else None

    def return_for_buttons_reader(self, reader: ReaderDB | None):
        if reader is None:
            return ForButtons()
        return ForButtons(
            is_reader=bool(reader),
            is_editor=reader.is_editor,
            is_author=reader.is_author
        ) 

    async def return_for_buttons(
        self,
        user: UserDB,
        purpose: UserDB | None = None,
        news_paper: NewsPaperDB | None = None,
    ) -> ForButtons:
        news_paper = news_paper or await self.check_exist_news_paper(self.news_paper_id)
        await news_paper.awaitable_attrs.readers
        reader = news_paper.reader_user_ids.get(user.id)
        purpose_reader_is_editor = news_paper.reader_user_ids.get(purpose.id).is_editor if purpose else False
        is_author = reader is not None and reader.is_author
        is_editor = reader is not None and reader.is_editor
        return ForButtons(
            is_reader=reader is not None,
            news_paper_id=news_paper.id,
            is_redact_setting=is_author,
            is_redact_rank=is_author,
            is_capture=reader is not None and news_paper.owner is None,
            is_give=is_author,
            is_news=is_editor,
            purpose_is_editor=purpose_reader_is_editor
        )
    
    async def return_news_paper_info(self, user: UserDB, news_paper: NewsPaperDB, for_buttons: ForButtons | None = None):
        readers = await news_paper.awaitable_attrs.readers
        return AnswerNewsPaperInfo(
            user=self.return_query_body(user),
            news_paper=NewsPaperInfo(
                id=news_paper.id,
                name=news_paper.name,
                owner=await self.return_reader_info(news_paper.owner) if news_paper.owner else None,
                emodzi=news_paper.emodzi,
                custom_emodzi_id=news_paper.custom_emodzi_id,
                reader_counts=len(readers),
            ),
            for_buttons=for_buttons
        )

    async def return_news_papers_info(self, news_papers: list[NewsPaperDB]):
        result = []
        for news_paper in news_papers:
            readers = await news_paper.awaitable_attrs.readers
            result.append(
                NewsPaperInfo(
                    id=news_paper.id,
                    name=news_paper.name,
                    owner=await self.return_reader_info(news_paper.owner) if news_paper.owner else None,
                    emodzi=news_paper.emodzi,
                    custom_emodzi_id=news_paper.custom_emodzi_id,
                    reader_counts=len(readers),
                )
            )
        return result



    async def all(self):
        data = await self.dao.news_paper.find_all()
        return AnswerAllNewsPaperInfo(news_papers=await self.return_news_papers_info(list(data)))

    async def news_papers_where_editor(self):
        user = await self.get_user(self.tg_id)
        await user.awaitable_attrs.readers
        return AnswerAllNewsPaperInfo(news_papers=await self.return_news_papers_info([r.news_paper for r in user.readers if r.is_editor]))

    async def news_papers_for_subscribe(self):
        data = await self.dao.news_paper.find_all()
        user = await self.get_user(self.tg_id)
        return AnswerAllNewsPaperInfo(news_papers=await self.return_news_papers_info([p for p in data if user.id not in p.reader_user_ids]))

    async def news_papers(self):
        user = await self.get_user(self.tg_id)
        await user.awaitable_attrs.readers
        return AnswerAllNewsPaperInfo(news_papers=await self.return_news_papers_info(list(user.news_papers.values())))

    async def search(self, value: str):
        news_papers = await self.dao.news_paper.search_by_name(value)
        return AnswerAllNewsPaperInfo(
            search_value=value,
            news_papers=await self.return_news_papers_info(news_papers),
        )

    async def info(self):
        user = await self.get_user(self.tg_id)
        news_paper = await self.check_exist_news_paper(self.news_paper_id)
        return await self.return_news_paper_info(
            user,
            news_paper,
            await self.return_for_buttons(user, news_paper=news_paper),
        )

    async def description(self):
        user = await self.get_user(self.tg_id)
        news_paper = await self.check_exist_news_paper(self.news_paper_id)
        return AnswerNewsPaperInfoDescription(
            user=self.return_query_body(user),
            id=news_paper.id,
            name=news_paper.name,
            description=news_paper.description,
        )

    async def readers(self):
        user = await self.get_user(self.tg_id)
        news_paper = await self.check_exist_news_paper(self.news_paper_id)
        readers = await self.dao.reader.get_members(news_paper.id)
        return AnswerNewsPaperInfoReaders(
            user=self.return_query_body(user),
            id=news_paper.id,
            name=news_paper.name,
            readers=[await self.return_reader_info(reader) for reader in readers],
        )

    async def reader(self):
        user = await self.get_user(only_user=True)
        purpose = await self.get_user(purpose_tg_id=self.purpose_tg_id)
        news_paper = await self.check_exist_news_paper(self.news_paper_id)
        await purpose.awaitable_attrs.readers
        reader = purpose.readers_by_news_paper_id.get(news_paper.id)
        if reader is None:
            raise ReaderError()
        return AnswerReaderInfo(
            user=self.return_query_body(purpose),
            reader=ReaderInfo(
                news_paper_name=news_paper.name,
                news_paper_id=news_paper.id,
                rank=reader.rank,
                rank_name=reader.rank_name,
            ),
            for_buttons=await self.return_for_buttons(user, purpose, news_paper),
        )





    async def create(self, name: str):
        user = await self.get_user(self.tg_id)
        news_paper = await self.dao.news_paper.add({"name": name})
        await user.awaitable_attrs.readers
        user.readers.append(ReaderDB(user=user, news_paper=news_paper, rank=AUTHOR_RANK))
        await self.dao.flush()
        self.botlog.newspaper_create(news_paper.name, news_paper.id)
        return await self.return_news_paper_info(user, news_paper)

    async def subscribe(self):
        user = await self.check_reader(self.tg_id, self.news_paper_id, False)
        news_paper = await self.check_exist_news_paper(self.news_paper_id)
        await user.awaitable_attrs.readers
        user.readers.append(ReaderDB(user=user, news_paper=news_paper))
        await self.dao.flush()
        self.botlog.newspaper_subscribe(news_paper.name, news_paper.id)
        return await self.return_news_paper_info(user, news_paper)

    async def unsubscribe(self):
        user = await self.check_reader(self.tg_id, self.news_paper_id)
        news_paper = await self.check_exist_news_paper(self.news_paper_id)
        await user.awaitable_attrs.readers
        if news_paper.id in user.news_papers:
            reader = user.readers_by_news_paper_id[news_paper.id]
            old_rank = reader.rank
            user.readers.remove(reader)
            await self.dao.flush()
            self.botlog.newspaper_unsubscribe(news_paper.name, news_paper.id, old_rank)
        return await self.return_news_paper_info(user, news_paper)

    async def settings(self):
        user, news_paper = await self.check_permission(
            self.news_paper_id,
            permission_rank=AUTHOR_RANK,
        )
        setting = NewsPaperSetting(news_paper.setting)
        return AnswerNewsPaperSetting(
            user=self.return_query_body(user),
            settings=setting.validate,
        )

    async def settings_values(self):
        user, news_paper = await self.check_permission(
            self.news_paper_id,
            permission_rank=AUTHOR_RANK,
        )
        setting = NewsPaperSetting(news_paper.setting)
        return AnswerNewsPaperSettingValues(
            user=self.return_query_body(user),
            values=setting.values,
        )

    async def settings_redact(self, parametrs: dict):
        user, news_paper = await self.check_permission(
            self.news_paper_id,
            permission_rank=AUTHOR_RANK,
        )
        setting = NewsPaperSetting(news_paper.setting)
        old_setting = setting.values
        setting.update(parametrs)
        news_paper.setting = setting.model_dump_db()
        self.dao.organ.update_obj(news_paper, news_paper.setting)
        await self.dao.flush()
        self.botlog.newspaper_setting(
            news_paper.name,
            news_paper.id,
            old_setting=old_setting,
            new_setting=setting.values,
        )
        return AnswerNewsPaperSetting(
            user=self.return_query_body(user),
            settings=setting.validate,
        )

    async def settings_default(self, default: OrganSettingDefault):
        user, news_paper = await self.check_permission(
            self.news_paper_id,
            permission_rank=AUTHOR_RANK,
        )
        setting = NewsPaperSetting(news_paper.setting)
        old_setting = setting.values
        if default.is_all:
            setting.to_default()
            news_paper.setting = {}
        elif default.group:
            news_paper.setting = setting.to_default(default.group)
        elif default.parametr:
            setting.check_tag({default.parametr: None})
            news_paper.setting = news_paper.setting.copy()
            news_paper.setting.pop(default.parametr, None)
            setting = NewsPaperSetting(news_paper.setting)
        else:
            raise ValueError('A setting parameter, group, or is_all must be specified')
        await self.dao.flush()
        self.botlog.newspaper_setting_default(
            news_paper.name,
            news_paper.id,
            old_setting=old_setting,
        )
        return AnswerNewsPaperSetting(
            user=self.return_query_body(user),
            settings=setting.validate,
        )



    async def notify(self):
        user, news_paper = await self.check_permission(self.news_paper_id, setting_parametr='editor_rank')
        await news_paper.awaitable_attrs.readers
        return AnswerNewsPaperInfoReaders(
            user=self.return_query_body(user),
            id=news_paper.id,
            name=news_paper.name,
            readers=[await self.return_reader_info(reader) for reader in news_paper.readers],
        )

    async def redact_rank(self, is_make: bool):
        await self.check_permission(self.news_paper_id, permission_rank=AUTHOR_RANK)
        purpose = await self.check_reader(self.purpose_tg_id, self.news_paper_id)
        news_paper = await self.check_exist_news_paper(self.news_paper_id)
        purpose_reader = news_paper.reader_user_ids.get(purpose.id)
        old_rank = purpose_reader.rank
        purpose_reader.rank = EDITOR_RANK if is_make else READER_RANK
        await self.dao.flush()
        self.botlog.newspaper_rank(news_paper.name, news_paper.id, old_rank, purpose_reader.rank)
        return AnswerRedactRank(
            user=self.return_query_body(purpose),
            new_rank=purpose_reader.rank,
            old_rank=old_rank,
            news_paper=NewsPaperInfo(
                id=news_paper.id,
                name=news_paper.name,
                owner=await self.return_reader_info(news_paper.owner) if news_paper.owner else None,
                emodzi=news_paper.emodzi,
                custom_emodzi_id=news_paper.custom_emodzi_id,
                reader_counts=len(news_paper.readers))
        )

    async def capture(self):
        user, news_paper = await self.check_permission(self.news_paper_id)
        await news_paper.awaitable_attrs.readers
        if news_paper.owner:
            raise NewsPaperPermissioError()

        reader = user.readers_by_news_paper_id[self.news_paper_id]
        old_rank = reader.rank
        reader.rank = AUTHOR_RANK
        await self.dao.flush()
        self.botlog.newspaper_capture(news_paper.name, news_paper.id, old_rank)
        return await self.return_news_paper_info(user, news_paper)

    async def give(self):
        user, news_paper = await self.check_permission(
            self.news_paper_id,
            permission_rank=AUTHOR_RANK,
        )
        purpose = await self.check_reader(self.purpose_tg_id, self.news_paper_id)
        if purpose.id == user.id:
            raise NewsPaperPermissioError()
        await purpose.awaitable_attrs.readers
        purpose_reader = purpose.readers_by_news_paper_id.get(self.news_paper_id)
        user_reader = user.readers_by_news_paper_id[self.news_paper_id]
        old_owner_tg_id = user.tg_id
        new_owner_tg_id = purpose.tg_id
        user_reader.rank = EDITOR_RANK
        purpose_reader.rank = AUTHOR_RANK
        await self.dao.flush()
        self.botlog.newspaper_give(
            news_paper.name,
            news_paper.id,
            old_owner_tg_id,
            new_owner_tg_id,
        )
        return AnswerNewsPaperGive(
            user=self.return_query_body(user),
            purpose=await self.return_reader_info(purpose_reader),
        )
