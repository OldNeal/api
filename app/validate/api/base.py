from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.db.models.main import UserDB
from datetime import datetime, timedelta
from typing import Literal, Any

THIS_NONE = object()

class BaseAPIValidate(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class QueryBody(BaseAPIValidate):
    tg_id: int
    username: str | None = THIS_NONE
    fullname: str | None = THIS_NONE

    @property
    def enter_body(self):
        return True if self.username != THIS_NONE and self.fullname != THIS_NONE else False 

class AnswerBody(BaseAPIValidate):
    pass

class AnswerUserBody(AnswerBody):
    tg_id: int

class AnswerBaseInfo(AnswerUserBody):
    name: str | None = None
    username: str | None = None

    path_name: str | None = None
    seq: int | None = None
    seq_name: str | None = None

    titul: str | None = None
    organ_name: str | None = None
    rank: int | None = None
    rank_name: str | None = None

    def to_query(self, data: UserDB):
        if data:
            self.name = data.name
            self.username = data.tg_user.username
            if data.beyonder:
                self.path_name = data.beyonder.seq.path.sequences.get(0).name
                self.seq = data.beyonder.seq_number
                self.seq_name = data.beyonder.seq_name
            if data.member:
                self.titul = data.member.titul
                self.organ_name = data.member.organ.name
                self.rank = data.member.rank
                self.rank_name = data.member.organ.rank_names.get(self.rank, 'Участник')
        return self
