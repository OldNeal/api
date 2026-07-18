from app.validate.api.base import AnswerBody, datetime
from app.db.models.beyonder import SequenceDB, PathDB, GreatAncientDB

class AnswerSeqInfo(AnswerBody):
    number: int
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



class AnswerSeqFullInfo(AnswerSeqInfo):
    path_name: str | None = None

    @classmethod
    def to_query(cls, data: SequenceDB):
        path_name = data.path.name
        return cls(path_name=path_name, seq_id=data.id, number=data.number, name=data.name, path_id=data.path_id)

class AnswerPathFullInfo(AnswerPathInfo):
    ga: AnswerGAInfo
    seqs: list[AnswerSeqInfo]

    @classmethod
    def to_query(cls, data: PathDB):
        ga = AnswerGAInfo(name=data.ga.name, ga_id=data.ga.id, group=data.ga.group)
        seqs = [AnswerSeqInfo(seq_id=s.id, number=s.number, name=s.name, path_id=data.id) for s in data.sequence_datas]
        return cls(ga=ga, ga_id=data.ga.id, seqs=seqs, name=data.name, group=data.ga.group, path_id=data.id)

class AnswerGAFullInfo(AnswerGAInfo):
    paths: list[AnswerPathInfo]

    @classmethod
    def to_query(cls, data: GreatAncientDB):
        paths = [AnswerPathInfo(name=p.name, path_id=p.id, group=data.group) for p in data.paths]
        return cls(name=data.name, ga_id=data.id, group=data.group, paths=paths)

class AnswerGroupInfo(AnswerBody):
    group_name: str
    gas: list[AnswerGAInfo] 

    @classmethod
    def to_query(cls, gas: list[GreatAncientDB]):
        group_name = gas[0].group
        gas = [AnswerGAInfo(name=g.name, ga_id=g.id, group=g.group) for g in gas]
        return cls(group_name=group_name, gas=gas)
    




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