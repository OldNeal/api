from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.db.models.main import UserDB
from datetime import datetime, timedelta
from typing import Literal, Any

class BaseAPIValidate(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class BaseBody(BaseAPIValidate):
    tg_id: int

class TelegramBody(BaseBody):
    username: str | None = None
    fullname: str | None = None

    @property
    def name(self):
        return self.fullname or self.username

class AnswerUserBody(BaseAPIValidate):
    user_id: int
    name: str | None = None
    telegram: TelegramBody | None = None

class QueryBody(BaseAPIValidate):
    user_id: int
    is_admin: bool = False
    request_id: str | None = None

class QueryUserUpdate(QueryBody):
    telegram: TelegramBody | None = None

class AnswerBaseBody(BaseAPIValidate):
    pass

class AnswerBody(AnswerBaseBody):
    user: AnswerUserBody
    purpose: AnswerUserBody | None = None

class BeyonderInfo(AnswerBaseBody):
    path_name: str | None = None
    seq: int | None = None
    seq_name: str | None = None
    emodzi: str | None = None
    custom_emodzi_id: str | None = None

class MemberInfo(AnswerBaseBody):
    titul: str | None = None
    organ_name: str | None = None
    organ_id: int | None = None
    rank: int | None = None
    rank_name: str | None = None
    login_at: str | None = None

class ReaderInfo(AnswerBaseBody):
    news_paper_name: str | None = None
    news_paper_id: int | None = None
    rank: int | None = None
    rank_name: str | None = None

class AnswerBaseInfo(AnswerBody):
    beyonder: BeyonderInfo | None = None
    member: MemberInfo | None = None

    def to_query(self, data: UserDB, beyonder: bool = True, member: bool = True):
        if data:
            if data.beyonder and beyonder:
                self.beyonder = BeyonderInfo(
                    path_name = data.beyonder.seq.path.god.name,
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

class ForButtons(AnswerBaseBody):
    is_member: bool = False
    is_reader: bool = False
    organ_id: int | None = None
    news_paper_id: int | None = None

    is_redact_setting: bool = False
    is_redact_rank: bool = False
    is_redact_titul: bool = False
    is_kick: bool = False
    is_capture: bool = False
    is_give: bool = False
    is_news: bool = False
    
class AnswerMain(AnswerBaseBody):
    message: str
    version: str

class AnswerLogFileNames(AnswerBaseBody):
    names: list[str]

class Page(BaseAPIValidate):
    number: int
    max: int

class AnswerUsersBody(AnswerBaseBody):
    search_value: str | int | None = None
    users: list[AnswerUserBody]
    page: Page | None = None
    count: int = 0