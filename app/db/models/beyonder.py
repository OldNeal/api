from sqlalchemy import ForeignKey, Integer, ARRAY, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal, ROUND_HALF_DOWN
from app.db.base import Base
from datetime import datetime
from app.logic.seq import sequences

class SequenceDB(Base):
    name: Mapped[str]
    number: Mapped[int]
    hash: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    path_id: Mapped[int | None] = mapped_column(ForeignKey('PathDB.id'))    
    path: Mapped['PathDB'] = relationship('PathDB', uselist=False, lazy='joined', back_populates='sequence_datas', cascade='all')
    _rsp_factor: Mapped[int | None] = mapped_column(name='rsp_factor', default=1, nullable=True)

    @property
    def rsp_factor(self):
        return self._rsp_factor if not self._rsp_factor is None else 1

    @property
    def all_rsp_factor(self):
        return self.rsp_factor*self.path.rsp_factor

    @property
    def in_dict(self):
        return ['_rsp_factor']

    @property
    def rsp(self):
        return sequences.get(self.number).rsp*self.all_rsp_factor

class PathDB(Base):
    hash: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    ga_id: Mapped[int] = mapped_column(ForeignKey('GreatAncientDB.id'))
    ga: Mapped['GreatAncientDB'] = relationship('GreatAncientDB', uselist=False, lazy='joined', back_populates='paths', cascade='all')
    sequence_datas: Mapped[list['SequenceDB']] = relationship('SequenceDB', uselist=True, lazy='select', back_populates='path', cascade='all')
    emodzi: Mapped[str | None] = mapped_column(default=None)
    custom_emodzi_id: Mapped[str | None] = mapped_column(default=None)
    god: Mapped[SequenceDB] = relationship('SequenceDB', uselist=False, lazy='joined', primaryjoin="and_(foreign(PathDB.id) == SequenceDB.path_id, SequenceDB.number == 0)", viewonly=True)
    _rsp_factor: Mapped[int | None] = mapped_column(name='rsp_factor', default=1, nullable=True)

    @property
    def rsp_factor(self):
        return self._rsp_factor if not self._rsp_factor is None else 1
    
    @property
    def sequences(self):
        return {s.number:s for s in self.sequence_datas} | {-1:self.ga}

    @property
    def name(self):
        return self.god.name

    @property
    def group(self):
        return self.ga.group

    @property
    def in_dict(self):
        return ['_rsp_factor']

    def model_dump(self):
        return {'name':self.name} | super().model_dump()
    
class GreatAncientDB(Base):
    name: Mapped[str]
    group: Mapped[str]
    hash: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    paths: Mapped[list['PathDB']] = relationship('PathDB', uselist=True, lazy='select', back_populates='ga', cascade='all')
    emodzi: Mapped[str | None] = mapped_column(default=None)
    custom_emodzi_id: Mapped[str | None] = mapped_column(default=None)
    
    @property
    def number(self):
        return -1

class BeyonderDB(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('UserDB.id'))
    user: Mapped[Base] = relationship('UserDB', uselist=False, lazy='select', back_populates='beyonder')
    seq_id: Mapped[int | None] = mapped_column(ForeignKey('SequenceDB.id'), nullable=True)
    seq: Mapped[SequenceDB] = relationship('SequenceDB', uselist=False, lazy='joined')
    ga_id: Mapped[int | None] = mapped_column(ForeignKey('GreatAncientDB.id'), nullable=True)
    ga: Mapped[GreatAncientDB] = relationship('GreatAncientDB', uselist=False, lazy='select')
    last_upseq: Mapped[datetime | None]
    next_upseq: Mapped[datetime | None]
    is_die: Mapped[bool] = mapped_column(default=False)
    _study_points: Mapped[int | None] = mapped_column(name='study_points', default=0, nullable=True)
    
    @property
    def seq_number(self):
        return -1 if self.ga_id else self.seq.number
    
    @property
    def seq_name(self):
        return self.ga.name if self.ga_id else self.seq.name

    @property
    def emodzi(self):
        return self.ga.emodzi if self.ga_id else self.seq.path.emodzi
    
    @property
    def custom_emodzi_id(self):
        return self.ga.custom_emodzi_id if self.ga_id else self.seq.path.custom_emodzi_id

    @property    
    def upseq_date(self):
        return (self.next_upseq - datetime.now()) if self.next_upseq else None
 
    @property
    def path_name(self):
        return self.seq.path.god.name

    @property
    def study_points(self):
        return self._study_points if self._study_points else 0

    @study_points.setter
    def study_points(self, points: int):
        self._study_points = points
        return self._study_points 
 
    def study_method_action(self, paths: int | None = None):
        if self.seq_number > -1 or paths is None:
            return (Decimal(10) / Decimal(self.seq.rsp)).quantize(Decimal('0.0001'), ROUND_HALF_DOWN)
        return (Decimal(10) / Decimal(self.seq.rsp*paths)).quantize(Decimal('0.0001'), ROUND_HALF_DOWN)