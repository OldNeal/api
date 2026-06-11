from app.logic.path import PathLogic
from app.service.base import BaseService

class PathService(BaseService):
    def __init__(self, session, tg_id: int | None = None):
        super().__init__(session, tg_id)
        self.logic = PathLogic(session, tg_id)

    async def path(self, seq_name: str):
        return await self.logic.path(seq_name)

    async def ga(self, seq_name: str):
        return await self.logic.ga(seq_name)

    async def search(self, value: str):
        return await self.logic.search(value)

    async def ga_search(self, value: str):
        return await self.logic.ga_search(value)

    async def group(self, group: str):
        return await self.logic.group(group)


