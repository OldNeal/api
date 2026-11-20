from app.validate.api.base import datetime, Literal, BaseAPIValidate, Any, AnswerBaseBody

class AnswerAllStats(AnswerBaseBody):
    users: int
    tg_users: int
    beyonders: int
    members: int
    organs: int
    paths: int
    gas: int
    news_papers: int
    questions: int
    activity_points_all_time: int
