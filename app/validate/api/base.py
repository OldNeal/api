from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.db.models.main import UserDB
from datetime import datetime, timedelta
from typing import Literal, Any

class BaseAPIValidate(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class BaseBody(BaseAPIValidate):
    tg_id: int

class QueryBody(BaseBody):
    tg_id: int
    username: str | None = None
    fullname: str | None = None
    is_admin: bool = False

    @property
    def enter_body(self):
        return True if self.username != None and self.fullname != None else False 

class AnswerBody(BaseAPIValidate):
    pass

class AnswerUserBody(AnswerBody):
    user: QueryBody

class AnswerBeyonderInfo(AnswerBody):
    path_name: str | None = None
    seq: int | None = None
    seq_name: str | None = None

class AnswerMemberInfo(AnswerBody):
    titul: str | None = None
    organ_name: str | None = None
    rank: int | None = None
    rank_name: str | None = None

class AnswerBaseInfo(AnswerUserBody):
    beyonder: AnswerBeyonderInfo | None = None
    member: AnswerMemberInfo | None = None

    def to_query(self, data: UserDB):
        if data:
            if data.beyonder:
                self.beyonder = AnswerBeyonderInfo(
                    path_name = data.beyonder.seq.path.sequences.get(0).name,
                    seq = data.beyonder.seq_number,
                    seq_name = data.beyonder.seq_name
                )
            if data.member:
                self.member = AnswerMemberInfo(
                    titul = data.member.titul,
                    organ_name = data.member.organ.name,
                    rank = data.member.rank,
                    rank_name = data.member.organ.rank_names.get(data.member.rank, 'Участник')
                )
        return self

class AnswerMain(AnswerBody):
    message: str
    version: str
