from app.logic.path import PathLogic
from app.service.base import BaseService

class PathService(BaseService):
    def __init__(self, session, tg_id: int | None = None):
        super().__init__(session, tg_id)
        self.logic = PathLogic(session, tg_id)

    async def path(self, seq_name: str | None = None, id: int | None = None):
        return await self.logic.path(seq_name, id)

    async def ga(self, seq_name: str | None = None, id: int | None = None):
        return await self.logic.ga(seq_name, id)

    async def group(self, group: str):
        return await self.logic.group(group)
    


    async def search(self, value: str):
        return await self.logic.search(value)

    async def ga_search(self, value: str):
        return await self.logic.ga_search(value)


    async def seqs(self):
        return await self.logic.seqs()
    
    async def paths(self):
        return await self.logic.paths()

    async def gas(self):
        return await self.logic.gas()

    async def groups(self):
        return await self.logic.groups()
