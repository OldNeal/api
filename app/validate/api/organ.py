from app.validate.api.base import datetime, Literal, BaseAPIValidate, Any, AnswerBody, AnswerUserBody, QueryBody, MemberInfo, UserDB
from app.validate.logic.setting import OrganSettingValidate

class AnswerOrganInfoBase(AnswerBody):
    id: int
    name: str

class ForButtons(AnswerBody):
    is_member: bool = False
    organ_id: int | None = None
    is_redact_setting: bool = False
    is_redact_rank: bool = False
    is_redact_titul: bool = False
    is_kick: bool = False
    is_capture: bool = False
    is_give: bool = False

class AnswerMemberInfo(AnswerUserBody):
    member: MemberInfo | None = None
    for_buttons: ForButtons | None = None

class OrganInfo(AnswerOrganInfoBase):
    owner: AnswerMemberInfo | None = None
    emodzi: str | None = None
    custom_emodzi_id: str | None = None
    member_counts: int = 0
    created_at: str

class AnswerOrganInfo(AnswerUserBody):
    organ: OrganInfo
    for_buttons: ForButtons | None = None

class AnswerOrganInfoMembers(AnswerOrganInfoBase, AnswerUserBody):
    members: list[AnswerMemberInfo]

class AnswerOrganInfoDescription(AnswerOrganInfoBase, AnswerUserBody):
    description: str | None = None

class AnswerAllOrganInfo(AnswerBody):
    search_value: str | None = None
    organs: list[OrganInfo]

class AnswerRedactRank(AnswerUserBody):
    new_rank: int
    old_rank: int

class AnswerRedactTitul(AnswerUserBody):
    new_titul: str | None = None
    old_titul: str | None = None

class AnswerOrganSetting(AnswerUserBody):
    settings: OrganSettingValidate

class AnswerOrganSettingValues(AnswerUserBody):
    values: dict

class QueryOrganSetting(QueryBody):
    parametrs: dict

class OrganSettingDefault(BaseAPIValidate):
    parametr: str | None = None
    group: str | None = None
    is_all: bool = False

class QueryOrganSettingDefault(QueryBody):
    to_default: OrganSettingDefault

class AnswerOrganGive(AnswerUserBody):
    purpose: AnswerMemberInfo