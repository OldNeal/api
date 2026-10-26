from app.exception.wiki import PathDontEnterFilterException
from app.logic.base import BaseLogic
from app.validate.api.wiki import (
    AnswerAllGAInfo,
    AnswerAllGroupInfo,
    AnswerAllPathInfo,
    AnswerAllSeqInfo,
    AnswerGAFullInfo,
    AnswerGASearchInfo,
    AnswerGroupInfo,
    AnswerPathFullInfo,
    AnswerPathSearchInfo,
    AnswerSeqFullInfo,
    AnswerSeqSearchInfo,
)


class PathLogic(BaseLogic):
    async def seq(self, name: str | None = None, id: int | None = None):
        if id is not None:
            data = await self.dao.sequence.query_by_id(id)
        elif name:
            data = await self.dao.sequence.query_by_name(name)
        else:
            raise PathDontEnterFilterException()
        return AnswerSeqFullInfo.to_query(data)

    async def path(self, name: str | None = None, id: int | None = None):
        if id is not None:
            data = await self.dao.path.query_by_id(id)
        elif name:
            data = await self.dao.path.query_by_name(name)
        else:
            raise PathDontEnterFilterException()
        return AnswerPathFullInfo.to_query(data)

    async def ga(self, name: str | None = None, id: int | None = None):
        if id is not None:
            data = await self.dao.greatancient.query_by_id(id)
        elif name:
            data = await self.dao.greatancient.query_by_name(name)
        else:
            raise PathDontEnterFilterException()
        return AnswerGAFullInfo.to_query(data)

    async def group(self, name: str):
        data = await self.dao.path.query_by_group(name)
        if not data:
            return AnswerGroupInfo(group_name=name, gas=[])
        return AnswerGroupInfo.to_query(data)

    async def search(self, name: str):
        data = await self.dao.path.search_by_name(name)
        paths = list({path.id: path for path in data}.values())
        return AnswerPathSearchInfo.to_query(name, paths)

    async def seq_search(self, name: str):
        terms = [term for term in name.casefold().split() if term]
        data = await self.dao.sequence.find_all()
        sequences = [
            sequence for sequence in data
            if any(term in sequence.name.casefold() for term in terms)
        ]
        return AnswerSeqSearchInfo.to_query(name, sequences)

    async def ga_search(self, name: str):
        data = await self.dao.greatancient.search_by_name(name)
        return AnswerGASearchInfo.to_query(name, data)

    async def seqs(self):
        data = await self.dao.sequence.find_all()
        return AnswerAllSeqInfo.to_query(data)

    async def paths(self):
        data = await self.dao.path.find_all()
        return AnswerAllPathInfo.to_query(data)

    async def gas(self):
        data = await self.dao.greatancient.find_all()
        return AnswerAllGAInfo.to_query(data)

    async def groups(self):
        data = await self.dao.greatancient.gropus()
        return AnswerAllGroupInfo(groups=data)

    async def seq_by_path_id(self, path_id: int, number: int):
        data = await self.dao.sequence.query_by_path_id(path_id, number)
        return AnswerSeqFullInfo.to_query(data)

    async def seqs_by_path_id(self, path_id: int):
        data = await self.dao.sequence.query_many_by_path_id(path_id)
        return AnswerAllSeqInfo.to_query(data)

    async def path_by_ga_id(self, ga_id: int):
        data = await self.dao.path.query_many_by_ga_id(ga_id)
        return AnswerAllPathInfo.to_query(data)
