from app.validate.api.base import AnswerUserBody, UserDB, datetime, QueryBody, timedelta, Literal, BaseAPIValidate, AnswerBody, BeyonderInfo, ForButtons
from app.validate.api.wiki import AnswerPathInfo

class Sequence(BaseAPIValidate):
    seq: str 
    number: int 
    path: str
    emodzi: str | None = None
    custom_emodzi_id: str | None = None

class AnswerRedactSeq(AnswerUserBody):
    old: Sequence | None = None
    new: Sequence | None = None
    operation: Literal['up', 'down', 'add']

class AnswerTimeInfo(AnswerUserBody):
    next_upseq: datetime | None
    last_upseq: datetime
    upseq_days: int | None

class AnswerTimeReplace(AnswerUserBody):
    old_time: datetime
    new_time: datetime

class AnswerTimeRedact(AnswerTimeReplace):
    seconds: int
    operator: Literal['-', '+']


class AnswerBeyonderInfo(AnswerUserBody):
    beyonder: BeyonderInfo | None = None
    for_buttons: ForButtons | None = None

    def to_query(self, data: UserDB):
        if data:
            if data.beyonder:
                self.beyonder = BeyonderInfo(
                    path_name = data.beyonder.seq.path.god.name,
                    seq = data.beyonder.seq_number,
                    seq_name = data.beyonder.seq_name,
                    emodzi=data.beyonder.emodzi, 
                    custom_emodzi_id=data.beyonder.custom_emodzi_id
                )
        return self

class AnswerBeyonderList(AnswerBody):
    path: AnswerPathInfo
    ga: AnswerBeyonderInfo | None = None
    beyonders: list[AnswerBeyonderInfo]
