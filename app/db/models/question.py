from sqlalchemy import String, BigInteger, ForeignKey, Numeric, JSON, inspect, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class QuestionDB(Base):
    body: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
    author_id: Mapped[int] = mapped_column(ForeignKey('EruditeDB.id'), default=None)
    author: Mapped['EruditeDB'] = relationship('EruditeDB', uselist=False, lazy='joined', back_populates='questions')
    answers: Mapped[list['AnswerQuestionDB']] = relationship('AnswerQuestionDB', uselist=True, lazy='joined', back_populates='question', cascade='all, delete-orphan')

    @property
    def answer_ids(self):
        return {answer.id:answer for answer in self.answers}
    
class AnswerQuestionDB(Base):
    __tablename__ = 'AnswerQuizDB'

    body: Mapped[str]
    question_id: Mapped[int] = mapped_column(ForeignKey('QuestionDB.id'))
    question: Mapped[QuestionDB] = relationship('QuestionDB', uselist=False, lazy='joined', back_populates='answers')
    is_correct: Mapped[bool]
    results: Mapped[list['ResultsQuestionDB']] = relationship('ResultsQuestionDB', uselist=True, lazy='select', back_populates='answer', cascade='all, delete-orphan')

class ResultsQuestionDB(Base):
    __tablename__ = 'ResultsQuizDB'

    erudite_id: Mapped[int] = mapped_column(ForeignKey('EruditeDB.id'))    
    erudite: Mapped['EruditeDB | None'] = relationship('EruditeDB', uselist=False, lazy='joined', back_populates='results')
    answer_id: Mapped[int] = mapped_column(ForeignKey('AnswerQuizDB.id'))
    answer: Mapped[AnswerQuestionDB] = relationship('AnswerQuestionDB', uselist=False, lazy='joined', back_populates='results')

class EruditeDB(Base):
    player_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('PlayerDB.id'))
    player: Mapped[Base] = relationship('PlayerDB', uselist=False, lazy='select', back_populates='erudite')
    results: Mapped[list[ResultsQuestionDB]] = relationship('ResultsQuestionDB', uselist=True, lazy='select', cascade='all, delete-orphan')
    questions: Mapped[list['QuestionDB']] = relationship('QuestionDB', uselist=True, lazy='select', back_populates='author', cascade='all')