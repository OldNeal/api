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

class BeyonderInfo(AnswerBody):
    path_name: str | None = None
    seq: int | None = None
    seq_name: str | None = None
    emodzi: str | None = None
    custom_emodzi_id: str | None = None

class MemberInfo(AnswerBody):
    titul: str | None = None
    organ_name: str | None = None
    organ_id: int | None = None
    rank: int | None = None
    rank_name: str | None = None
    login_at: str | None = None

class AnswerBaseInfo(AnswerUserBody):
    beyonder: BeyonderInfo | None = None
    member: MemberInfo | None = None

    def to_query(self, data: UserDB, beyonder: bool = True, member: bool = True):
        if data:
            if data.beyonder and beyonder:
                self.beyonder = BeyonderInfo(
                    path_name = data.beyonder.seq.path.sequences.get(0).name,
                    seq = data.beyonder.seq_number,
                    seq_name = data.beyonder.seq_name,
                    emodzi=data.beyonder.emodzi, 
                    custom_emodzi_id=data.beyonder.custom_emodzi_id
                )
            if data.member and member:
                self.member = MemberInfo(
                    titul = data.member.titul,
                    organ_name = data.member.organ.name,
                    rank = data.member.rank,
                    rank_name = data.member.organ.rank_names.get(data.member.rank, 'Участник'),
                    login_at=data.member.created_at.isoformat()
                )
        return self



class AnswerMain(AnswerBody):
    message: str
    version: str
