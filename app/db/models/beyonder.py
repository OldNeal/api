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
        return {s.number:s for s in self.sequence_datas}

class GreatAncientDB(Base):
    name: Mapped[str]
    paths: Mapped[list['PathDB']] = relationship('PathDB', uselist=True, lazy='select', back_populates='ga', cascade='all')

class BeyonderDB(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('UserDB.id'))
    seq_id: Mapped[int] = mapped_column(ForeignKey('SequenceDB.id'), nullable=True)
    seq: Mapped[SequenceDB] = relationship('SequenceDB', uselist=False, lazy='joined')
    ga_id: Mapped[int] = mapped_column(ForeignKey('GreatAncientDB.id'), nullable=True)
    ga: Mapped[GreatAncientDB] = relationship('GreatAncientDB', uselist=False, lazy='select')
    upseq_data: Mapped[datetime | None]
    is_die: Mapped[bool] = mapped_column(default=False)
    
    @property
    def seq_number(self):
        return -1 if self.ga_id else self.seq.number
    
    @property
    def seq_name(self):
        return self.ga.name if self.ga_id else self.seq.name