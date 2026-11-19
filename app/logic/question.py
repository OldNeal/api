import random
from datetime import datetime, timedelta

from config import MAX_DAILY_QUESTION_ANSWERS
from app.logic.activity import ActivityLogic
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
from app.exception.question import (
    AnswerDontFindException,
    QuestionAlreadyAnsweredException,
    QuestionDailyLimitException,
    QuestionDontFindException,
)

class QuestionLogic(ActivityLogic):
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

    async def check_daily_question_limit(self, erudite_id: int):
        answered_today = await self.dao.results_question.count_answered_today(erudite_id)
        if answered_today >= MAX_DAILY_QUESTION_ANSWERS:
            raise QuestionDailyLimitException()

    def question_body(
        self,
        question: QuestionDB,
        show_correct: bool = False,
        answers: list[AnswerQuestionDB] | None = None,
    ):
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
                for answer in (question.answers if answers is None else answers)
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
        if answer.is_correct:
            last_answered_at = await self.dao.results_question.last_answered_at(
                user.player.erudite.id,
                answer_id,
            )
            if last_answered_at and last_answered_at > datetime.now() - timedelta(days=14):
                raise QuestionAlreadyAnsweredException()
        await self.check_daily_question_limit(user.player.erudite.id)
        await user.player.erudite.awaitable_attrs.results
        user.player.erudite.results.append(ResultsQuestionDB(answer_id=answer_id))
        await self.dao.flush()
        if answer.is_correct:
            item, activity_points = await self.get_activity_points_question()
        else:
            activity_points = 0
        return AnswerQuestionAnswer(
            user=self.return_query_body(user),
            purpose=self.return_query_body(user),
            answer_id=answer_id,
            is_correct=answer.is_correct,
            question=self.question_body(
                question,
                show_correct=question.author_id == user.player.erudite.id,
            ),
            activity_points=activity_points
        )

    async def answer_the_question_incorrect(self, question_id: int):
        question = await self.check_question(question_id)
        answer = next(
            (answer for answer in question.answers if not answer.is_correct),
            None,
        )
        if answer is None:
            raise AnswerDontFindException()

        user = await self.check_erudite(self.user_id)
        await self.check_daily_question_limit(user.player.erudite.id)
        await user.player.erudite.awaitable_attrs.results
        user.player.erudite.results.append(ResultsQuestionDB(answer_id=answer.id))
        await self.dao.flush()
        return AnswerQuestionAnswer(
            user=self.return_query_body(user),
            purpose=self.return_query_body(user),
            answer_id=answer.id,
            is_correct=False,
            question=self.question_body(
                question,
                show_correct=question.author_id == user.player.erudite.id,
            ),
        )

    async def answer_the_question_wrong(self, question_id: int):
        return await self.answer_the_question_incorrect(question_id)

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

    async def random_question(self, correct_count: int = 1, incorrect_count: int = 3):
        user = await self.check_erudite(self.user_id)
        erudite_id = user.player.erudite.id
        now = datetime.now()
        answered_after = now - timedelta(days=14)
        incorrect_answered_after = now - timedelta(days=3)
        question = await self.dao.question.find_random_with_answer_counts(
            correct_count,
            incorrect_count,
            erudite_id,
            answered_after,
            incorrect_answered_after,
        )
        if question is None:
            raise QuestionDontFindException('Вопросы пока что закончились')
        recently_answered_ids = set(await self.dao.question.recently_answered_correct_ids(
            erudite_id,
            question.id,
            answered_after,
        ))
        correct_answers = [
            answer
            for answer in question.answers
            if answer.is_correct and answer.id not in recently_answered_ids
        ]
        incorrect_answers = [answer for answer in question.answers if not answer.is_correct]
        answers = random.sample(correct_answers, correct_count) + random.sample(
            incorrect_answers,
            incorrect_count,
        )
        random.shuffle(answers)
        return AnswerRandomQuestion(
            question=self.question_body(question, answers=answers),
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

        