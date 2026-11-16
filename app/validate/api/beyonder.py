from app.validate.api.base import AnswerBaseBody, UserDB, datetime, QueryBody, timedelta, Literal, BaseAPIValidate, AnswerBody, BeyonderInfo, ForButtons, Page
from app.validate.api.wiki import AnswerPathInfo

class Sequence(BaseAPIValidate):
    seq: str 
    number: int 
    path: str
    path_id: int
    ga_id: int
    emodzi: str | None = None
    custom_emodzi_id: str | None = None

class AnswerRedactSeq(AnswerBody):
    old: Sequence | None = None
    new: Sequence | None = None
    operation: Literal['up', 'down', 'add']

class TimeReplace(AnswerBaseBody):
    old_time: datetime
    new_time: datetime

class TimeRedact(TimeReplace):
    seconds: int
    operator: Literal['-', '+']

class AnswerTimeReplace(AnswerBody, TimeReplace):
    pass

class AnswerTimeRedact(AnswerBody, TimeRedact):
    pass


class AnswerBeyonderInfo(AnswerBody):
    beyonder: BeyonderInfo | None = None
    points: 'Points | None' = None
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

class AnswerTimeInfo(AnswerBeyonderInfo):
    next_upseq: datetime | None
    last_upseq: datetime
    total_seconds: float | None

class AnswerBeyonderList(AnswerBaseBody):
    path: AnswerPathInfo
    ga: AnswerBeyonderInfo | None = None
    beyonders: list[AnswerBeyonderInfo]
    page: Page | None = None
    count: int = 0

class Point(AnswerBaseBody):
    old: int | None = None
    new: int

class Points(AnswerBaseBody):
    study_points: Point
    activity_points: Point
    rsp: int
    study_method_action: float

class AnswerStudyMethodAction(AnswerBeyonderInfo):
    time: TimeRedact
