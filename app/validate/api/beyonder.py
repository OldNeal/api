from app.validate.api.base import AnswerUserBody, datetime, QueryBody, timedelta, Literal, BaseAPIValidate

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


