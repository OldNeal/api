from sqlalchemy import ForeignKey, Integer, ARRAY, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime
    
class SequenceDB(Base):
    name: Mapped[str]
    number: Mapped[int]
    path_id: Mapped[int | None] = mapped_column(ForeignKey('PathDB.id'))    
    path: Mapped['PathDB'] = relationship('PathDB', uselist=False, lazy='joined', back_populates='sequence_datas', cascade='all')

class PathDB(Base):
    ga_id: Mapped[int] = mapped_column(ForeignKey('GreatAncientDB.id'))
    ga: Mapped['GreatAncientDB'] = relationship('GreatAncientDB', uselist=False, lazy='joined', back_populates='paths', cascade='all')
    sequence_datas: Mapped[list['SequenceDB']] = relationship('SequenceDB', uselist=True, lazy='select', back_populates='path', cascade='all')

    @property
    def sequences(self):
        return {s.number:s for s in self.sequence_datas} | {-1:self.ga}

    @property
    def name(self):
        return self.sequences.get(0).name

class GreatAncientDB(Base):
    name: Mapped[str]
    group: Mapped[str]
    paths: Mapped[list['PathDB']] = relationship('PathDB', uselist=True, lazy='select', back_populates='ga', cascade='all')

    @property
    def number(self):
        return -1

class BeyonderDB(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('UserDB.id'))
    seq_id: Mapped[int | None] = mapped_column(ForeignKey('SequenceDB.id'), nullable=True)
    seq: Mapped[SequenceDB] = relationship('SequenceDB', uselist=False, lazy='joined')
    ga_id: Mapped[int | None] = mapped_column(ForeignKey('GreatAncientDB.id'), nullable=True)
    ga: Mapped[GreatAncientDB] = relationship('GreatAncientDB', uselist=False, lazy='select')
    last_upseq: Mapped[datetime | None]
    next_upseq: Mapped[datetime | None]
    is_die: Mapped[bool] = mapped_column(default=False)
    
    @property
    def seq_number(self):
        return -1 if self.ga_id else self.seq.number
    
    @property
    def seq_name(self):
        return self.ga.name if self.ga_id else self.seq.name

    @property
    def upseq_days(self):
        return (self.next_upseq.date() - datetime.now().date()).days if self.next_upseq else None

    @property
    def path_name(self):
        return self.seq.path.sequences.get(0).name

