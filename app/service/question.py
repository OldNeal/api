from app.logic.question import QuestionLogic
from app.service.base import BaseService
from app.validate.api.question import QueryQuestionCreate


class QuestionService(BaseService):
    def __init__(self, session, user_id: int | None = None, purpose_user_id: int | None = None, is_admin: bool = False):
        super().__init__(session, user_id, purpose_user_id, is_admin)
        self.logic = QuestionLogic(session, user_id=user_id, purpose_user_id=purpose_user_id, is_admin=self.is_admin)

    async def create_question(self, data: QueryQuestionCreate):
        return await self.logic.create_question(data)

    async def answer_the_question(self, question_id: int, answer_id: int):
        return await self.logic.answer_the_question(question_id, answer_id)

    async def search(self, value: str, page: int | None = None, per_page: int = 5):
        return await self.logic.search(value, page, per_page)

    async def list(self, page: int | None = None, per_page: int = 5):
        return await self.logic.list(page, per_page)

    async def random_question(self):
        return await self.logic.random_question()

    async def my_questions(self, page: int | None = None, per_page: int = 5):
        return await self.logic.my_questions(page, per_page)

    async def statistics(self, question_id: int):
        return await self.logic.statistics(question_id)

    async def user_answer_statistics(self):
        return await self.logic.user_answer_statistics()
