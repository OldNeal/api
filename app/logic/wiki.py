from app.logic.base import BaseLogic
from app.logic.utils import class_decor

@class_decor
class WikiLogic(BaseLogic):
    async def seq(self, name: str | None = None, id: int | None = None):
        return await self.client.get_seq(name, id)

    async def path(self, seq_name: str | None = None, id: int | None = None):
        return await self.client.get_path(seq_name, id)

    async def ga(self, seq_name: str | None = None, id: int | None = None):
        return await self.client.get_ga(seq_name, id)

    async def group(self, group: str):
        return await self.client.get_group(group)
    


    async def path_search(self, value: str, page: int | None = None, per_page: int = 5):
        return await self.client.search_path(value, page, per_page)

    async def seq_search(self, value: str, page: int | None = None, per_page: int = 5):
        print(self.client.client.config.headers)
        return await self.client.search_seq(value, page, per_page)

    async def ga_search(self, value: str, page: int | None = None, per_page: int = 5):
        return await self.client.search_ga(value, page, per_page)


    async def seqs(self, page: int | None = None, per_page: int = 5):
        return await self.client.get_seqs(page, per_page)
    
    async def paths(self, page: int | None = None, per_page: int = 5):
        return await self.client.get_paths(page, per_page)

    async def gas(self, page: int | None = None, per_page: int = 5):
        return await self.client.get_gas(page, per_page)

    async def groups(self, page: int | None = None, per_page: int = 5):
        return await self.client.get_groups(page, per_page)


    async def seq_by_path_id(self, path_id: int, number: int):
        return await self.client.get_seq_by_path_id(path_id, number)

    async def seqs_by_path_id(self, path_id: int, page: int | None = None, per_page: int = 5):
        return await self.client.get_seqs_by_path_id(path_id, page, per_page)

    async def path_by_ga_id(self, ga_id: int, page: int | None = None, per_page: int = 5):
        return await self.client.get_path_by_ga_id(ga_id, page, per_page)
