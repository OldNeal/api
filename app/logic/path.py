from app.logic.base import BaseLogic


class PathLogic(BaseLogic):
    async def path(self, name: str):
        return await self.dao.path.query_by_name(name)
        
    async def ga(self, name: str):
        return await self.dao.greatancient.query_by_name(name)

    async def group(self, name: str):
        return await self.dao.path.query_by_group(name)

    async def search(self, name: str):
        return await self.dao.path.search_by_name(name)
    
    async def ga_search(self, name: str):
        return await self.dao.greatancient.search_by_name(name)

