from app.validate.api.base import datetime, Literal, BaseAPIValidate, Any, AnswerBody, AnswerBaseBody, QueryBody, MemberInfo, UserDB, ForButtons, Page
from app.validate.logic.setting import OrganSettingValidate

class AnswerOrganInfoBase(AnswerBaseBody):
    id: int
    name: str

class AnswerMemberInfo(AnswerBody):
    member: MemberInfo | None = None
    for_buttons: ForButtons | None = None

class OrganInfo(AnswerOrganInfoBase):
    owner: AnswerMemberInfo | None = None
    emodzi: str | None = None
    custom_emodzi_id: str | None = None
    member_counts: int = 0
    created_at: str

class AnswerOrganInfo(AnswerBody):
    organ: OrganInfo
    for_buttons: ForButtons | None = None

class AnswerOrganInfoMembers(AnswerOrganInfoBase, AnswerBody):
    members: list[AnswerMemberInfo]
    page: Page | None = None
    count: int = 0

class AnswerOrganInfoDescription(AnswerOrganInfoBase, AnswerBody):
    description: str | None = None

class AnswerAllOrganInfo(AnswerBaseBody):
    search_value: str | None = None
    organs: list[OrganInfo]
    page: Page | None = None
    count: int = 0

class AnswerRedactRank(AnswerBody):
    new_rank: int
    old_rank: int

class AnswerRedactTitul(AnswerBody):
    new_titul: str | None = None
    old_titul: str | None = None

class AnswerOrganSetting(AnswerBody):
    settings: OrganSettingValidate

class AnswerOrganSettingValues(AnswerBody):
    values: dict

class QueryOrganSetting(QueryBody):
    parametrs: dict

class OrganSettingDefault(BaseAPIValidate):
    parametr: str | None = None
    group: str | None = None
    is_all: bool = False

class QueryOrganSettingDefault(QueryBody):
    to_default: OrganSettingDefault

class AnswerOrganGive(AnswerBody):
    pass