from app.validate.api.base import datetime, Literal, BaseAPIValidate, Any, AnswerBaseBody

class AnswerAllStats(AnswerBaseBody):
    users: int
    beyonders: int
    members: int
    organs: int
    paths: int
    gas: int
