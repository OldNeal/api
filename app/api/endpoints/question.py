from fastapi import APIRouter, Depends, Query
from app.api.depends.session import get_session
from app.exception import get_exception_codes
from app.service.question import QuestionService
from app.validate.api.base import QueryBody
from app.validate.api.question import (
    AnswerAllQuestions,
    AnswerQuestion,
    AnswerQuestionAnswer,
    AnswerQuestionSearch,
    AnswerQuestionStatistics,
    AnswerRandomQuestion,
    AnswerUserQuestionStatistics,
    QueryQuestionCreate,
)

question_router = APIRouter(prefix='/question', tags=['question'], responses=get_exception_codes(types=['question']))


@question_router.post('/create', response_model=AnswerQuestion)
async def question_create(
    query: QueryQuestionCreate,
    session=Depends(get_session()),
):
    return await QuestionService(session, user_id=query.user_id, is_admin=query.is_admin).create_question(query)


@question_router.post('/answer', response_model=AnswerQuestionAnswer)
async def question_answer(
    query: QueryBody,
    question_id: int = Query(description='ID вопроса'),
    answer_id: int = Query(description='ID ответа'),
    session=Depends(get_session()),
):
    return await QuestionService(session, user_id=query.user_id, is_admin=query.is_admin).answer_the_question(
        question_id,
        answer_id,
    )


@question_router.post('/search', response_model=AnswerQuestionSearch, response_model_exclude_none=True)
async def question_search(
    query: QueryBody,
    value: str = Query(description='Текст для поиска вопроса'),
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
    session=Depends(get_session()),
):
    return await QuestionService(session, user_id=query.user_id, is_admin=query.is_admin).search(value, page, per_page)


@question_router.post('/list', response_model=AnswerAllQuestions, response_model_exclude_none=True)
async def question_list(
    query: QueryBody,
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
    session=Depends(get_session()),
):
    return await QuestionService(session, user_id=query.user_id, is_admin=query.is_admin).list(page, per_page)

@question_router.post('/random', response_model=AnswerRandomQuestion, response_model_exclude_none=True)
async def question_random(
    query: QueryBody,
    session=Depends(get_session()),
):
    return await QuestionService(session, user_id=query.user_id, is_admin=query.is_admin).random_question()


@question_router.post('/my', response_model=AnswerAllQuestions, response_model_exclude_none=True)
async def question_my(
    query: QueryBody,
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
    session=Depends(get_session()),
):
    return await QuestionService(session, user_id=query.user_id, is_admin=query.is_admin).my_questions(page, per_page)


@question_router.post('/statistics', response_model=AnswerQuestionStatistics)
async def question_statistics(
    query: QueryBody,
    question_id: int = Query(description='ID вопроса'),
    session=Depends(get_session()),
):
    return await QuestionService(session, user_id=query.user_id, is_admin=query.is_admin).statistics(question_id)


@question_router.post('/statistics/user', response_model=AnswerUserQuestionStatistics)
async def question_user_statistics(
    query: QueryBody,
    session=Depends(get_session()),
):
    return await QuestionService(
        session,
        user_id=query.user_id,
        is_admin=query.is_admin,
    ).user_answer_statistics()
