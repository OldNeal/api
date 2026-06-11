from app.validate.api.base import AnswerUserBody, datetime, QueryBody

class AnswerInfoUpseq(AnswerUserBody):
    next_upseq: datetime
    last_upseq: datetime
    upseq_days: int



