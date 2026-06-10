from sqlalchemy import ForeignKey, Integer, ARRAY, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime
    
class SequenceDB(Base):
    name: Mapped[str]
    seq: Mapped[int]
    path_id: Mapped[int | None] = mapped_column(ForeignKey('PathDB.id'))    
    path: Mapped['PathDB'] = relationship('PathDB', uselist=False, lazy='joined', back_populates='sequence_datas')

class PathDB(Base):
    name: Mapped[str]
    ga_id: Mapped[int] = mapped_column(ForeignKey('GreatAncientDB.id'))
    ga: Mapped['GreatAncientDB'] = relationship('GreatAncientDB', uselist=False, lazy='joined', back_populates='paths')
    sequence_datas: Mapped[list['SequenceDB']] = relationship('SequenceDB', uselist=True, lazy='select', back_populates='path')

    @property
    def sequences(self):
        return {s.seq:s for s in self.sequence_datas}

class GreatAncientDB(Base):
    name: Mapped[str]
    paths: Mapped[list['PathDB']] = relationship('PathDB', uselist=True, lazy='select', back_populates='ga')

class BeyonderDB(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('UserDB.id'))
    seq_id: Mapped[int] = mapped_column(ForeignKey('SequenceDB.id'))
    upseq: Mapped[datetime]
    is_die: Mapped[bool] = mapped_column(default=False)
    