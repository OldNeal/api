from sqlalchemy import String, BigInteger, ForeignKey, Numeric, JSON, inspect, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.db.models.question import EruditeDB    

class PlayerDB(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('UserDB.id'))
    user: Mapped[Base] = relationship('UserDB', uselist=False, lazy='select', back_populates='player')
    erudite: Mapped[EruditeDB | None] = relationship('EruditeDB', uselist=False, lazy='joined', back_populates='player', cascade='all, delete-orphan')
