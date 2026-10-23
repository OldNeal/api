from app.logic.newspaper import NewsPaperLogic
from app.service.base import BaseService


class NewsPaperService(BaseService):
    def __init__(self, session, tg_id: int | None = None, purpose_tg_id: int | None = None, news_paper_id: int | None = None, is_admin: bool = False,):
        super().__init__(session, tg_id, purpose_tg_id, is_admin)
        self.logic = NewsPaperLogic(session, tg_id=tg_id, purpose_tg_id=purpose_tg_id, news_paper_id=news_paper_id, is_admin=self.is_admin,)

    async def all(self):
        return await self.logic.all()
    
    async def news_papers_where_editor(self):
        return await self.logic.news_papers_where_editor()

    async def news_papers_for_subscribe(self):
        return await self.logic.news_papers_for_subscribe()
    
    async def news_papers(self):
        return await self.logic.news_papers()

    async def search(self, value: str):
        return await self.logic.search(value)

    async def info(self):
        return await self.logic.info()

    async def readers(self):
        return await self.logic.readers()

    async def reader(self):
        return await self.logic.reader()

    async def create(self, name: str):
        return await self.logic.create(name)

    async def subscribe(self):
        return await self.logic.subscribe()

    async def unsubscribe(self):
        return await self.logic.unsubscribe()

    async def notify(self):
        return await self.logic.notify()

    async def make_editor(self):
        return await self.logic.redact_rank(True)

    async def fire_editor(self):
        return await self.logic.redact_rank(False)

    async def capture(self):
        return await self.logic.capture()

    async def give(self):
        return await self.logic.give()

    async def settings(self):
        return await self.logic.settings()

    async def settings_values(self):
        return await self.logic.settings_values()

    async def settings_redact(self, parametrs: dict):
        return await self.logic.settings_redact(parametrs)

    async def settings_default(self, default):
        return await self.logic.settings_default(default)
