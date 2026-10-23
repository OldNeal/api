from sqlalchemy import String, BigInteger, ForeignKey, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

AUTHOR_RANK = 0
EDITOR_RANK = 1
READER_RANK = 2

class NewsPaperDB(Base):
    name: Mapped[str] = mapped_column(String(50))
    emodzi: Mapped[str | None] = mapped_column(default=None)
    custom_emodzi_id: Mapped[str | None] = mapped_column(default=None)
    description: Mapped[str | None] = mapped_column(default=None)
    readers: Mapped[list['ReaderDB']] = relationship('ReaderDB', uselist=True, lazy='select', back_populates='news_paper', cascade='all, delete-orphan')
    setting: Mapped[dict] = mapped_column(JSON, default={})

    @property
    def owner(self):
        for reader in self.readers:
            if reader.rank == AUTHOR_RANK:
                return reader

    @classmethod
    def default_rank_name(cls):
        return {
        '2':'Читатель',
        '1':'Редактор',
        '0':'Автор',
    }

    @property
    def rank_names(self) -> dict[int, str]:
        return {int(k):v for k,v in self.setting.get('rank_names', self.default_rank_name()).items()}

    @property
    def reader_user_ids(self):
        return {r.user_id:r for r in self.readers}

class ReaderDB(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('UserDB.id'))
    user: Mapped[Base] = relationship('UserDB', uselist=False, lazy='select', back_populates='readers')
    titul: Mapped[str | None] = mapped_column(String(30))
    news_paper_id: Mapped[int] = mapped_column(ForeignKey('NewsPaperDB.id'))
    news_paper: Mapped[NewsPaperDB] = relationship('NewsPaperDB', uselist=False, lazy='joined', back_populates='readers')
    rank: Mapped[int] = mapped_column(default=READER_RANK)
    receive_notifications: Mapped[bool] = mapped_column(default=True)
    
    @property
    def rank_name(self):
        return self.news_paper.rank_names.get(self.rank, 'Чтатель') 

    @property
    def is_editor(self):
        return self.rank <= self.news_paper.setting.get('editor_rank', EDITOR_RANK)
    
    @property
    def is_author(self):
        return self.rank == AUTHOR_RANK