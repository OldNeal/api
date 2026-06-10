from sqlalchemy import String, BigInteger, ForeignKey, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

class OrganDB(Base):
    name: Mapped[str] = mapped_column(String(50), unique=True)
    owner: Mapped[int] = mapped_column(ForeignKey('UserDB.id'))
    organ: Mapped['OrganPermissionDB'] = relationship('OrganPermissionDB', uselist=False, lazy='joined')
    name_ranks: Mapped[dict[int, str]] = mapped_column(JSON, default={
        9:'Новичок',
        8:'Участник',
        7:'Участник',
        6:'Участник',
        5:'Участник',
        4:'Старший',
        3:'Старший',
        2:'Советник',
        1:'Советник',
        0:'Глава',
    })

class OrganPermissionDB(Base):
    organ: Mapped[int] = mapped_column(ForeignKey('OrganDB.id'))

class MemberDB(Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('UserDB.id'))
    titul: Mapped[str | None] = mapped_column(String(30))
    organ_id: Mapped[int] = mapped_column(ForeignKey('OrganDB.id'))
    organ: Mapped[OrganDB] = relationship('OrganDB', uselist=False, lazy='joined')
    rank: Mapped[int] = mapped_column(default=9)
    
    
    