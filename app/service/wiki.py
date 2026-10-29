from app.logic.wiki import PathLogic
from app.service.base import BaseService

class PathService(BaseService):
    def __init__(self, session, user_id: int | None = None, purpose_user_id: int | None = None, is_admin: bool = False):
        super().__init__(session, user_id, purpose_user_id, is_admin)
        self.logic = PathLogic(session, user_id)

    async def seq(self, name: str | None = None, id: int | None = None):
        return await self.logic.seq(name, id)

    async def path(self, seq_name: str | None = None, id: int | None = None):
        return await self.logic.path(seq_name, id)

    async def ga(self, seq_name: str | None = None, id: int | None = None):
        return await self.logic.ga(seq_name, id)

    async def group(self, group: str):
        return await self.logic.group(group)
    


    async def search(self, value: str, page: int | None = None, per_page: int = 5):
        return await self.logic.search(value, page, per_page)

    async def seq_search(self, value: str, page: int | None = None, per_page: int = 5):
        return await self.logic.seq_search(value, page, per_page)

    async def ga_search(self, value: str, page: int | None = None, per_page: int = 5):
        return await self.logic.ga_search(value, page, per_page)


    async def seqs(self, page: int | None = None, per_page: int = 5):
        return await self.logic.seqs(page, per_page)
    
    async def paths(self, page: int | None = None, per_page: int = 5):
        return await self.logic.paths(page, per_page)

    async def gas(self, page: int | None = None, per_page: int = 5):
        return await self.logic.gas(page, per_page)

    async def groups(self, page: int | None = None, per_page: int = 5):
        return await self.logic.groups(page, per_page)


    async def seq_by_path_id(self, path_id: int, number: int):
        return await self.logic.seq_by_path_id(path_id, number)

    async def seqs_by_path_id(self, path_id: int, page: int | None = None, per_page: int = 5):
        return await self.logic.seqs_by_path_id(path_id, page, per_page)

    async def path_by_ga_id(self, ga_id: int, page: int | None = None, per_page: int = 5):
        return await self.logic.path_by_ga_id(ga_id, page, per_page)
