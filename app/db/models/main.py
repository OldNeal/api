from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.db.models.beyonder import BeyonderDB
from app.db.models.organ import MemberDB

class TgUserDB(Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str]
    username: Mapped[str | None] = mapped_column(default=None)
    data: Mapped[dict] = mapped_column(JSON)

class TgChatDB(Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    type: Mapped[str]
    fullname: Mapped[str]
    username: Mapped[str | None] = mapped_column(default=None)
    data: Mapped[dict] = mapped_column(JSON)

class UserDB(Base):
    tg_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, default=None)
    _name: Mapped[str | None] = mapped_column(name='name', default=None)
    is_ban: Mapped[bool] = mapped_column(default=False)
    tg_user: Mapped[TgUserDB] = relationship(TgUserDB, uselist=False, lazy='joined', primaryjoin="foreign(TgUserDB.tg_id) == UserDB.tg_id")
    beyonder: Mapped[BeyonderDB] = relationship('BeyonderDB', uselist=False, lazy='joined')
    member: Mapped[MemberDB] = relationship('MemberDB', uselist=False, lazy='joined')

    @property
    def name(self):
        return self._name if self._name else self.tg_user.fullname

class ChatDB(Base):
    tg_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, default=None)
    tg_chat: Mapped[TgChatDB | None] = relationship(TgChatDB, uselist=False, lazy='joined', primaryjoin="foreign(TgChatDB.tg_id) == ChatDB.tg_id")
    is_ban: Mapped[bool] = mapped_column(default=False)
