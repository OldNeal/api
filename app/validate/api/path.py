from app.validate.api.base import AnswerBody, datetime
from app.db.models.beyonder import SequenceDB, PathDB, GreatAncientDB

class AnswerSeqInfo(AnswerBody):
    seq: int
    name: str
    path_id: int
    seq_id: int

class AnswerPathInfo(AnswerBody):
    group: str
    name: str
    path_id: int

class AnswerGAInfo(AnswerBody):
    group: str
    name: str
    ga_id: int





class AnswerPathFullInfo(AnswerBody):
    ga_name: str | None = None
    seqs: list[AnswerSeqInfo] | None = None
    name: str | None = None

    @classmethod
    def to_query(cls, data: PathDB):
        if data:
            ga_name = data.ga.name
            seqs = [AnswerSeqInfo(seq_id=s.id, seq=s.number, name=s.name, path_id=data.id) for s in data.sequence_datas]
            return cls(ga_name=ga_name, seqs=seqs, name=data.name)
        return cls()

class AnswerGAFullInfo(AnswerBody):
    ga_name: str | None = None
    paths: list[AnswerPathInfo] | None = None

    @classmethod
    def to_query(cls, data: GreatAncientDB):
        if data:
            ga_name = data.name
            paths = [AnswerPathInfo(name=p.name, path_id=p.id, group=data.group) for p in data.paths]
            return cls(ga_name=ga_name, paths=paths)
        return cls()

class AnswerGroupInfo(AnswerBody):
    group_name: str | None = None
    gas: list[AnswerGAInfo] | None = None

    @classmethod
    def to_query(cls, gas: list[GreatAncientDB]):
        if gas:
            group_name = gas[0].group
            new_paths = [AnswerGAInfo(name=g.name, ga_id=g.id, group=g.group) for g in gas]
            return cls(group_name=group_name, gas=new_paths)
        return cls()
    




class AnswerSeqSearchInfo(AnswerBody):
    search_value: str | None = None
    seqs: list[AnswerPathInfo] | None = None

    @classmethod
    def to_query(cls, search_value: str, seqs: list[SequenceDB]):
        if seqs:
            seqs = [AnswerSeqInfo(seq_id=s.id, seq=s.number, name=s.name, path_id=s.path_id) for s in seqs]
            return cls(search_value=search_value, seqs=seqs)
        return cls(search_value=search_value)
    
class AnswerPathSearchInfo(AnswerBody):
    search_value: str | None = None
    paths: list[AnswerPathInfo] | None = None

    @classmethod
    def to_query(cls, search_value: str, paths: list[PathDB]):
        if paths:
            paths = [AnswerPathInfo(name=p.name, path_id=p.id, group=p.ga.group) for p in paths]
            return cls(search_value=search_value, paths=paths)
        return cls(search_value=search_value)

class AnswerGASearchInfo(AnswerBody):
    search_value: str | None = None
    gas: list[AnswerGAInfo] | None = None
    
    @classmethod
    def to_query(cls, search_value: str, gas: list[GreatAncientDB]):
        if gas:
            new_gas = [AnswerGAInfo(name=g.name, ga_id=g.id, group=g.group) for g in gas]
            return cls(search_value=search_value, gas=new_gas)
        return cls(search_value=search_value)
    






class AnswerAllSeqInfo(AnswerBody):
    seqs: list[AnswerSeqInfo] | None = None

    @classmethod
    def to_query(cls, seqs: list[SequenceDB]):
        if seqs:
            seqs = [AnswerSeqInfo(seq_id=s.id, seq=s.number, name=s.name, path_id=s.path_id) for s in seqs]
            return cls(seqs=seqs)
        return cls()
    
class AnswerAllPathInfo(AnswerBody):
    paths: list[AnswerPathInfo] | None = None

    @classmethod
    def to_query(cls, paths: list[PathDB]):
        if paths:
            paths = [AnswerPathInfo(name=p.name, path_id=p.id, group=p.ga.group) for p in paths]
            return cls(paths=paths)
        return cls()

class AnswerAllGAInfo(AnswerBody):
    gas: list[AnswerGAInfo] | None = None
    
    @classmethod
    def to_query(cls, gas: list[GreatAncientDB]):
        if gas:
            new_gas = [AnswerGAInfo(name=g.name, ga_id=g.id, group=g.group) for g in gas]
            return cls(gas=new_gas)
        return cls()
    
class AnswerAllGroupInfo(AnswerBody):
    groups: list[str]