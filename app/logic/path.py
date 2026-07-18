from app.logic.base import BaseLogic
from app.exception.wiki import PathDontEnterFilterException

class PathLogic(BaseLogic):
    async def seq(self, name: str | None = None, id: int | None = None):
        if id:
            return await self.dao.sequence.query_by_id(id)
        elif name: 
            return await self.dao.sequence.query_by_name(name)
        raise PathDontEnterFilterException()
    
    async def path(self, name: str | None = None, id: int | None = None):
        if id:
            return await self.dao.path.query_by_id(id)
        elif name: 
            return await self.dao.path.query_by_name(name)
        raise PathDontEnterFilterException()

    async def ga(self, name: str | None = None, id: int | None = None):
        if id:
            return await self.dao.greatancient.query_by_id(id)
        elif name: 
            return await self.dao.greatancient.query_by_name(name)
        raise PathDontEnterFilterException()

    async def group(self, name: str):
        return await self.dao.path.query_by_group(name)



    async def search(self, name: str):
        return await self.dao.path.search_by_name(name)
    
    async def ga_search(self, name: str):
        return await self.dao.greatancient.search_by_name(name)



    async def seqs(self):
        return await self.dao.sequence.find_all()
    
    async def paths(self):
        return await self.dao.path.find_all()

    async def gas(self):
        return await self.dao.greatancient.find_all()

    async def groups(self):
        return await self.dao.greatancient.gropus()



    async def seq_by_path_id(self, path_id: int, number: int):
        return await self.dao.sequence.query_by_path_id(path_id, number)

    async def seqs_by_path_id(self, path_id: int):
        return await self.dao.sequence.query_many_by_path_id(path_id)

    async def path_by_ga_id(self, ga_id: int):
        return await self.dao.path.query_many_by_ga_id(ga_id)
