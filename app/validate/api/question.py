from app.validate.api.base import AnswerBaseBody, AnswerBody, BaseAPIValidate, Page, QueryBody

class QustionBase(BaseAPIValidate):
    body: str
    description: str | None = None

class QuestionCreate(QustionBase):
    correct_answers: list[str]
    incorrect_answers: list[str]

class QueryQuestionCreate(QueryBody):
    purpose_user_id: int | None = None
    question: QuestionCreate

class QuestionAnswer(BaseAPIValidate):
    answer_id: int
    body: str
    is_correct: bool | None = None

class Question(QustionBase):
    question_id: int
    answers: list[QuestionAnswer]

class AnswerQuestionAnswer(AnswerBody):
    answer_id: int
    question: Question

class AnswerQuestion(AnswerBody):
    question: Question

class AnswerAllQuestions(AnswerBaseBody):
    questions: list[Question]
    page: Page | None = None
    count: int = 0

class AnswerRandomQuestion(AnswerBaseBody):
    question: Question

class AnswerQuestionSearch(AnswerAllQuestions):
    search_value: str

class QuestionAnswerStatistics(QuestionAnswer):
    count: int

class AnswerQuestionStatistics(AnswerBody):
    question_id: int
    answers: list[QuestionAnswerStatistics]
    statistics: 'UserQuestionStatistics'

class UserQuestionStatistics(BaseAPIValidate):
    total: int
    correct: int
    incorrect: int
    accuracy: float

class AnswerUserQuestionStatistics(AnswerBody):
    statistics: UserQuestionStatistics