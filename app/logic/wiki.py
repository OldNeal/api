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
        data = await self.dao.greatancient.get_by_group(name)
        return AnswerGroupInfo.to_query(name, data)

    async def search(self, name: str, page: int | None = None, per_page: int = 5):
        data, count = await self.dao.path.search_by_name_paginated(name, page, per_page)
        paths = list({path.id: path for path in data}.values())
        return AnswerPathSearchInfo.to_query(
            name,
            paths,
            self.pagination(page, per_page, count),
            count,
        )

    async def seq_search(self, name: str, page: int | None = None, per_page: int = 5):
        sequences, count = await self.dao.sequence.search_by_name_paginated(name, page, per_page)
        return AnswerSeqSearchInfo.to_query(
            name,
            sequences,
            self.pagination(page, per_page, count),
            count,
        )

    async def ga_search(self, name: str, page: int | None = None, per_page: int = 5):
        data, count = await self.dao.greatancient.search_by_name_paginated(name, page, per_page)
        return AnswerGASearchInfo.to_query(
            name,
            data,
            self.pagination(page, per_page, count),
            count,
        )

    async def seqs(self, page: int | None = None, per_page: int = 5):
        data, count = await self.dao.sequence.find_all_paginated(page=page, per_page=per_page)
        return AnswerAllSeqInfo.to_query(data, self.pagination(page, per_page, count), count)

    async def paths(self, page: int | None = None, per_page: int = 5):
        data, count = await self.dao.path.find_all_paginated(page=page, per_page=per_page)
        return AnswerAllPathInfo.to_query(data, self.pagination(page, per_page, count), count)

    async def gas(self, page: int | None = None, per_page: int = 5):
        data, count = await self.dao.greatancient.find_all_paginated(page=page, per_page=per_page)
        return AnswerAllGAInfo.to_query(data, self.pagination(page, per_page, count), count)

    async def groups(self, page: int | None = None, per_page: int = 5):
        data, count = await self.dao.greatancient.groups_paginated(page, per_page)
        return AnswerAllGroupInfo(
            groups=data,
            page=self.pagination(page, per_page, count),
            count=count,
        )

    async def seq_by_path_id(self, path_id: int, number: int):
        data = await self.dao.sequence.query_by_path_id(path_id, number)
        return AnswerSeqFullInfo.to_query(data)

    async def seqs_by_path_id(self, path_id: int, page: int | None = None, per_page: int = 5):
        data, count = await self.dao.sequence.query_many_by_path_id_paginated(
            path_id,
            page,
            per_page,
        )
        return AnswerAllSeqInfo.to_query(data, self.pagination(page, per_page, count), count)

    async def path_by_ga_id(self, ga_id: int, page: int | None = None, per_page: int = 5):
        data, count = await self.dao.path.query_many_by_ga_id_paginated(
            ga_id,
            page,
            per_page,
        )
        return AnswerAllPathInfo.to_query(data, self.pagination(page, per_page, count), count)
