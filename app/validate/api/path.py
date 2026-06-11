from app.validate.api.base import AnswerBody, datetime
from app.db.models.beyonder import SequenceDB, PathDB, GreatAncientDB

class AnswerSeqInfo(AnswerBody):
    seq: int
    name: str

class AnswerPathInfo(AnswerBody):
    ga_name: str | None = None
    seqs: list[AnswerSeqInfo] | None = None

    @classmethod
    def to_query(cls, data: PathDB):
        if data:
            ga_name = data.ga.name
            seqs = [AnswerSeqInfo(seq=s.number, name=s.name) for s in data.sequence_datas]
            return cls(ga_name=ga_name, seqs=seqs)
        return cls()

class AnswerGAInfo(AnswerBody):
    ga_name: str | None = None
    paths: list[AnswerPathInfo] | None = None

    @classmethod
    def to_query(cls, data: GreatAncientDB):
        if data:
            ga_name = data.name
            paths = [AnswerPathInfo.to_query(p) for p in data.paths]
            return cls(ga_name=ga_name, paths=paths)
        return cls()

class AnswerGroupInfo(AnswerBody):
    group_name: str | None = None
    paths: list[AnswerPathInfo] | None = None

    @classmethod
    def to_query(cls, paths: list[PathDB]):
        if paths:
            group_name = paths[0].ga.group
            new_paths = [AnswerPathInfo.to_query(p) for p in paths]
            return cls(group_name=group_name, paths=new_paths)
        return cls()

class AnswerPathSearchInfo(AnswerBody):
    search_value: str | None = None
    seqs: list[AnswerPathInfo] | None = None

    @classmethod
    def to_query(cls, search_value: str, datas: list[PathDB]):
        if datas:
            seqs = [AnswerPathInfo.to_query(data) for data in datas]
            return cls(search_value=search_value, seqs=seqs)
        return cls(search_value=search_value)

class AnswerGASearchInfo(AnswerBody):
    search_value: str | None = None
    gas: list[AnswerGAInfo] | None = None
    
    @classmethod
    def to_query(cls, search_value: str, gas: list[GreatAncientDB]):
        if gas:
            new_gas = [AnswerGAInfo.to_query(g) for g in gas]
            return cls(search_value=search_value, gas=new_gas)
        return cls(search_value=search_value)