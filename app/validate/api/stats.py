from app.validate.api.base import datetime, Literal, BaseAPIValidate, Any, AnswerBody

class AnswerAllStats(AnswerBody):
    users: int
    beyonders: int
    members: int
    organs: int
    paths: int
    gas: int
