from app.validate.api.base import AnswerBaseBody, datetime, Page
from app.db.models.beyonder import SequenceDB, PathDB, GreatAncientDB

class AnswerSeqInfo(AnswerBaseBody):
    number: int
    name: str
    path_id: int
    seq_id: int

class AnswerPathInfo(AnswerBaseBody):
    group: str
    name: str
    path_id: int
    emodzi: str | None = None
    custom_emodzi_id: str | None = None

class AnswerGAInfo(AnswerBaseBody):
    group: str
    name: str
    ga_id: int
    emodzi: str | None = None
    custom_emodzi_id: str | None = None



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
        ga = AnswerGAInfo(name=data.ga.name, ga_id=data.ga.id, group=data.group, emodzi=data.ga.emodzi, custom_emodzi_id=data.ga.custom_emodzi_id)
        seqs = [AnswerSeqInfo(seq_id=s.id, number=s.number, name=s.name, path_id=data.id) for s in data.sequence_datas]
        return cls(ga=ga, ga_id=data.ga.id, seqs=seqs, name=data.name, group=data.group, path_id=data.id, emodzi=data.emodzi, custom_emodzi_id=data.custom_emodzi_id)

class AnswerGAFullInfo(AnswerGAInfo):
    paths: list[AnswerPathInfo]

    @classmethod
    def to_query(cls, data: GreatAncientDB):
        paths = [AnswerPathInfo(name=p.name, path_id=p.id, group=data.group, emodzi=p.emodzi, custom_emodzi_id=p.custom_emodzi_id) for p in data.paths]
        return cls(name=data.name, ga_id=data.id, group=data.group, paths=paths, emodzi=data.emodzi, custom_emodzi_id=data.custom_emodzi_id)

class AnswerGroupInfo(AnswerBaseBody):
    group_name: str
    gas: list[AnswerGAInfo] 

    @classmethod
    def to_query(cls, group_name: str, gas: list[GreatAncientDB]):
        gas = [AnswerGAInfo(name=g.name, ga_id=g.id, group=g.group, emodzi=g.emodzi, custom_emodzi_id=g.custom_emodzi_id) for g in gas]
        return cls(group_name=group_name, gas=gas)
    




class AnswerSeqSearchInfo(AnswerBaseBody):
    search_value: str | None = None
    seqs: list[AnswerSeqInfo] | None = None
    page: Page | None = None
    count: int = 0

    @classmethod
    def to_query(cls, search_value: str, seqs: list[SequenceDB], page: Page | None = None, count: int = 0):
        if seqs:
            seqs = [AnswerSeqInfo(seq_id=s.id, number=s.number, name=s.name, path_id=s.path_id) for s in seqs]
            return cls(search_value=search_value, seqs=seqs, page=page, count=count)
        return cls(search_value=search_value, seqs=[], page=page, count=count)
    
class AnswerPathSearchInfo(AnswerBaseBody):
    search_value: str | None = None
    paths: list[AnswerPathInfo] | None = None
    page: Page | None = None
    count: int = 0

    @classmethod
    def to_query(cls, search_value: str, paths: list[PathDB], page: Page | None = None, count: int = 0):
        if paths:
            paths = [AnswerPathInfo(name=p.name, path_id=p.id, group=p.group, emodzi=p.emodzi, custom_emodzi_id=p.custom_emodzi_id) for p in paths]
            return cls(search_value=search_value, paths=paths, page=page, count=count)
        return cls(search_value=search_value, paths=[], page=page, count=count)

class AnswerGASearchInfo(AnswerBaseBody):
    search_value: str | None = None
    gas: list[AnswerGAInfo] | None = None
    page: Page | None = None
    count: int = 0
    
    @classmethod
    def to_query(cls, search_value: str, gas: list[GreatAncientDB], page: Page | None = None, count: int = 0):
        if gas:
            new_gas = [AnswerGAInfo(name=g.name, ga_id=g.id, group=g.group, emodzi=g.emodzi, custom_emodzi_id=g.custom_emodzi_id) for g in gas]
            return cls(search_value=search_value, gas=new_gas, page=page, count=count)
        return cls(search_value=search_value, gas=[], page=page, count=count)
    






class AnswerAllSeqInfo(AnswerBaseBody):
    seqs: list[AnswerSeqInfo] | None = None
    page: Page | None = None
    count: int = 0

    @classmethod
    def to_query(cls, seqs: list[SequenceDB], page: Page | None = None, count: int = 0):
        if seqs:
            seqs = [AnswerSeqInfo(seq_id=s.id, number=s.number, name=s.name, path_id=s.path_id) for s in seqs]
            return cls(seqs=seqs, page=page, count=count)
        return cls(seqs=[], page=page, count=count)
    
class AnswerAllPathInfo(AnswerBaseBody):
    paths: list[AnswerPathInfo] | None = None
    page: Page | None = None
    count: int = 0

    @classmethod
    def to_query(cls, paths: list[PathDB], page: Page | None = None, count: int = 0):
        if paths:
            paths = [AnswerPathInfo(name=p.name, path_id=p.id, group=p.group, emodzi=p.emodzi, custom_emodzi_id=p.custom_emodzi_id) for p in paths]
            return cls(paths=paths, page=page, count=count)
        return cls(paths=[], page=page, count=count)

class AnswerAllGAInfo(AnswerBaseBody):
    gas: list[AnswerGAInfo] | None = None
    page: Page | None = None
    count: int = 0
    
    @classmethod
    def to_query(cls, gas: list[GreatAncientDB], page: Page | None = None, count: int = 0):
        if gas:
            new_gas = [AnswerGAInfo(name=g.name, ga_id=g.id, group=g.group, emodzi=g.emodzi, custom_emodzi_id=g.custom_emodzi_id) for g in gas]
            return cls(gas=new_gas, page=page, count=count)
        return cls(gas=[], page=page, count=count)
    
class AnswerAllGroupInfo(AnswerBaseBody):
    groups: list[str]
    page: Page | None = None
    count: int = 0