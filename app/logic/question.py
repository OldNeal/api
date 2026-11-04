from app.logic.base import BaseLogic
from app.validate.api.question import (
    AnswerAllQuestions,
    AnswerQuestion,
    AnswerQuestionAnswer,
    AnswerQuestionSearch,
    AnswerQuestionStatistics,
    AnswerRandomQuestion,
    AnswerUserQuestionStatistics,
    Question,
    QuestionAnswer,
    QuestionAnswerStatistics,
    QueryQuestionCreate,
    UserQuestionStatistics
)
from app.db.models.question import AnswerQuestionDB, EruditeDB, QuestionDB, ResultsQuestionDB
from app.db.models.player import PlayerDB
from app.exception.base import ParametrValidationException, PermissionException
from app.exception.question import AnswerDontFindException, QuestionDontFindException

class QuestionLogic(BaseLogic):
    async def check_erudite(self, user_id: int | None):
        if user_id is None:
            raise ParametrValidationException('Не указан ID пользователя')
        user = await self.get_user(user_id)
        if user.player is None:
            user.player = PlayerDB(user_id=user.id)
        if user.player.erudite is None:
            user.player.erudite = EruditeDB()
        await self.dao.flush()
        return user

    async def check_question(self, question_id: int):
        question = await self.dao.question.find_one_or_none_by_id(question_id)
        if question is None:
            raise QuestionDontFindException()
        return question

    def question_body(self, question: QuestionDB, show_correct: bool = False):
        return Question(
            question_id=question.id,
            body=question.body,
            description=question.description,
            answers=[
                QuestionAnswer(
                    answer_id=answer.id,
                    body=answer.body,
                    is_correct=answer.is_correct if show_correct else None,
                )
                for answer in question.answers
            ],
        )

    async def questions_response(self, questions: list[QuestionDB]):
        return [
            self.question_body(question, show_correct=True)
            for question in questions
        ]

    async def create_question(self, data: QueryQuestionCreate):
        user = await self.check_erudite(self.check_is_not_none(self.purpose_user_id, self.user_id))
        question = QuestionDB(
            body=data.question.body,
            description=data.question.description
        )
        await user.player.erudite.awaitable_attrs.questions
        user.player.erudite.questions.append(question)
        question.answers.extend([
            AnswerQuestionDB(
                body=answer, 
                is_correct=True) for answer in data.question.correct_answers])
        question.answers.extend([
            AnswerQuestionDB(
                body=answer, 
                is_correct=False) for answer in data.question.incorrect_answers])
        await self.dao.flush()
        self.botlog.question_create(question.id, user.id)
        return AnswerQuestion(
            user=self.return_query_body(user),
            purpose=self.return_query_body(user),
            question=self.question_body(question, show_correct=True),
        )

    async def answer_the_question(self, question_id: int, answer_id: int):
        question = await self.check_question(question_id)
        answer = question.answer_ids.get(answer_id)
        if answer is None:
            raise AnswerDontFindException()
        user = await self.check_erudite(self.user_id)
        await user.player.erudite.awaitable_attrs.results
        user.player.erudite.results.append(ResultsQuestionDB(answer_id=answer_id))
        await self.dao.flush()
        return AnswerQuestionAnswer(
            user=self.return_query_body(user),
            purpose=self.return_query_body(user),
            answer_id=answer_id,
            question=self.question_body(
                question,
                show_correct=question.author_id == user.player.erudite.id,
            ),
        )

    async def search(self, value: str, page: int | None = None, per_page: int = 5):
        if not value.strip():
            raise ParametrValidationException('Укажите текст для поиска вопроса')
        questions, count = await self.dao.question.search_paginated(value, page, per_page)
        return AnswerQuestionSearch(
            search_value=value,
            questions=await self.questions_response(questions),
            page=self.pagination(page, per_page, count),
            count=count,
        )

    async def list(self, page: int | None = None, per_page: int = 5):
        questions, count = await self.dao.question.find_all_paginated(page=page, per_page=per_page)
        return AnswerAllQuestions(
            questions=await self.questions_response(questions),
            page=self.pagination(page, per_page, count),
            count=count,
        )

    async def random_question(self):
        question = await self.dao.question.find_random()
        if question is None:
            raise QuestionDontFindException()
        return AnswerRandomQuestion(
            question=(await self.questions_response([question]))[0],
        )

    async def my_questions(self, page: int | None = None, per_page: int = 5):
        if self.user_id is None:
            raise ParametrValidationException('Не указан ID пользователя')
        questions, count = await self.dao.question.find_for_user_paginated(
            self.user_id,
            page,
            per_page,
        )
        return AnswerAllQuestions(
            questions=[self.question_body(question, show_correct=True) for question in questions],
            page=self.pagination(page, per_page, count),
            count=count,
        )

    async def statistics(self, question_id: int):
        question = await self.check_question(question_id)
        user = await self.get_user(self.user_id)
        if user.player is None or user.player.erudite is None or user.player.erudite.id != question.author_id:
            raise PermissionException()
        answers = await self.dao.question.answer_statistics(question_id)
        correct_count = sum(count for _, _, is_correct, count in answers if is_correct)
        incorrect_count = sum(count for _, _, is_correct, count in answers if not is_correct)
        total_count = correct_count + incorrect_count
        return AnswerQuestionStatistics(
            user=self.return_query_body(user),
            purpose=self.return_query_body(user),
            question_id=question_id,
            answers=[
                QuestionAnswerStatistics(
                    answer_id=answer_id,
                    body=body,
                    is_correct=is_correct,
                    count=count,
                )
                for answer_id, body, is_correct, count in answers
            ],
            statistics=UserQuestionStatistics(
                total=total_count,
                correct=correct_count,
                incorrect=incorrect_count,
                accuracy=round(correct_count / total_count * 100, 2) if total_count else 0,
            ),
        )

    async def user_answer_statistics(self):
        if self.user_id is None:
            raise ParametrValidationException('Не указан ID пользователя')
        user = await self.get_user(self.user_id)
        statistics = await self.dao.results_question.statistics_by_user(self.user_id)
        correct_answers = statistics.get(True, 0)
        incorrect_answers = statistics.get(False, 0)
        total_answers = correct_answers + incorrect_answers
        accuracy = round(correct_answers / total_answers * 100, 2) if total_answers else 0
        return AnswerUserQuestionStatistics(
            user=self.return_query_body(user),
            purpose=self.return_query_body(user),
            statistics=UserQuestionStatistics(
                total=total_answers,
                correct=correct_answers,
                incorrect=incorrect_answers,
                accuracy=accuracy
            )
        )

        