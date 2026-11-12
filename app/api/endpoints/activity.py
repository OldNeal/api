from fastapi import APIRouter, Depends, Query, Header
from app.api.depends.session import get_session
from app.exception import get_exception_codes
from app.service.activity import ActivityService
from app.validate.api.base import (
    AnswerActivityPoints,
    AnswerActivityPointsAdd,
    AnswerActivityPointsDeduct,
    AnswerActivityPointsLimitReset,
    QueryBody,
)

activity_router = APIRouter(
    prefix='/activity',
    tags=['activity'],
    responses=get_exception_codes(types=['activity']),
)


@activity_router.patch('/messages', response_model=AnswerActivityPoints)
async def activity_points(
    query: QueryBody,
    message_count: int = Query(1, description='Количество сообщений'),
    session=Depends(get_session()),
):
    return await ActivityService(
        session,
        user_id=query.user_id,
        is_admin=query.is_admin,
    ).get_activity_points(message_count)


@activity_router.patch('/points/add', response_model=AnswerActivityPointsAdd)
async def activity_points_add(
    query: QueryBody,
    user_id: int = Query(description='ID пользователя, которому начисляются очки'),
    points: int = Query(gt=0, description='Количество очков для начисления'),
    reason: str | None = Query(None, max_length=500, description='Причина начисления очков'),
    session=Depends(get_session()),
):
    return await ActivityService(
        session,
        user_id=query.user_id,
        purpose_user_id=user_id,
        is_admin=query.is_admin,
    ).add_activity_points(user_id, points, reason)


@activity_router.patch('/points/deduct', response_model=AnswerActivityPointsDeduct)
async def activity_points_deduct(
    query: QueryBody,
    user_id: int = Query(description='ID пользователя, у которого снимаются очки'),
    points: int = Query(gt=0, description='Количество очков для снятия'),
    reason: str | None = Query(None, max_length=500, description='Причина снятия очков'),
    session=Depends(get_session()),
):
    return await ActivityService(
        session,
        user_id=query.user_id,
        purpose_user_id=user_id,
        is_admin=query.is_admin,
    ).deduct_activity_points(user_id, points, reason)


@activity_router.patch('/points/reset', response_model=AnswerActivityPoints)
async def activity_points_reset(
    query: QueryBody,
    user_id: int = Query(description='ID пользователя, баланс которого сбрасывается'),
    reason: str | None = Query(None, max_length=500, description='Причина сброса баланса'),
    session=Depends(get_session()),
):
    return await ActivityService(
        session,
        user_id=query.user_id,
        purpose_user_id=user_id,
        is_admin=query.is_admin,
    ).reset_activity_points(user_id, reason)


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
