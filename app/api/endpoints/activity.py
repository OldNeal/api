from fastapi import APIRouter, Depends, Query
from app.api.depends.session import get_session
from app.exception import get_exception_codes
from app.service.activity import ActivityService
from app.validate.api.base import (
    AnswerActivityPoints,
    AnswerActivityPointsLimit,
    AnswerActivityPointsLimitReset,
    QueryBody,
)

activity_router = APIRouter(
    prefix='/activity',
    tags=['activity'],
    responses=get_exception_codes(types=['activity', 'item']),
)


@activity_router.patch('', response_model=AnswerActivityPoints)
async def activity_points(
    query: QueryBody,
    message_count: int = Query(1, description='Количество сообщений'),
    session=Depends(get_session()),
):
    return await ActivityService(
        session,
        user_id=query.user_id,
        is_admin=query.is_admin,
    ).get_activity_points_message(message_count)


@activity_router.get('/points', response_model=AnswerActivityPoints)
async def activity_points_count(
    user_id: int = Query(description='ID пользователя'),
    session=Depends(get_session()),
):
    return await ActivityService(session, user_id=user_id).get_activity_points_count()


@activity_router.get('/limit', response_model=AnswerActivityPointsLimit)
async def activity_points_limit(
    user_id: int = Query(description='ID пользователя'),
    session=Depends(get_session()),
):
    return await ActivityService(session, user_id=user_id).get_activity_points_limit()


@activity_router.patch('/limit/reset', response_model=AnswerActivityPointsLimitReset)
async def activity_points_limit_reset(
    query: QueryBody,
    user_id: int = Query(description='ID пользователя, для которого сбрасывается лимит'),
    session=Depends(get_session()),
):
    return await ActivityService(
        session,
        user_id=query.user_id,
        purpose_user_id=user_id,
        is_admin=query.is_admin,
    ).reset_activity_points_limit(user_id)
