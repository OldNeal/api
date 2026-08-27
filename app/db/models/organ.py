from sqlalchemy import String, BigInteger, ForeignKey, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

class OrganDB(Base):
    name: Mapped[str] = mapped_column(String(50))
    emodzi: Mapped[str | None] = mapped_column(default=None)
    custom_emodzi_id: Mapped[str | None] = mapped_column(default=None)
    description: Mapped[str | None] = mapped_column(default=None)
    members: Mapped[list['MemberDB']] = relationship('MemberDB', uselist=True, lazy='select', back_populates='organ', cascade='all, delete-orphan')
    setting: Mapped[dict] = mapped_column(JSON, default={})

    @property
    def owner_id(self):
        for member in self.members:
            if member.rank == 0:
                return member.user_id
            
    @property
    def owner(self):
        for member in self.members:
            if member.rank == 0:
                return member

    @classmethod
    def default_rank_name(cls):
        return {
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
    }

    @property
    def rank_names(self) -> dict[int, str]:
        return {int(k):v for k,v in self.setting.get('rank_names', self.default_rank_name()).items()}

class MemberDB(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('UserDB.id'))
    titul: Mapped[str | None] = mapped_column(String(30))
    organ_id: Mapped[int] = mapped_column(ForeignKey('OrganDB.id'))
    organ: Mapped[OrganDB] = relationship('OrganDB', uselist=False, lazy='joined', cascade='all')
    rank: Mapped[int] = mapped_column(default=9)
    
    @property
    def rank_name(self):
        return self.organ.rank_names.get(self.rank, 'Участник')
    