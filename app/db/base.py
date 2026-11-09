from datetime import datetime
from typing import Iterable
from sqlalchemy import Integer, func, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__

    def model_dump(self):
        return {k:v for k,v in sorted(self.__dict__.items(), key=lambda x: x[0], reverse=True) if not k.startswith('_') or k in self.in_dict}
    
    @property
    def in_dict(self):
        return []

    def model_dump_json(self):
        return {k:v for k,v in self.model_dump().items() if self.moderate_type(v)}

    def moderate_type(self, value):
        if isinstance(value, Iterable) and not isinstance(value, str):
            return all([self.moderate_type(v) for v in value])
        return all([not isinstance(value, t) for t in [datetime, Base]])