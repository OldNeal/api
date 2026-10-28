from fastapi import APIRouter, Depends, Query, Path
from app.validate.api.base import QueryBody, AnswerBaseInfo, QueryUserUpdate, AnswerUserBody, AnswerUsersBody
from app.api.endpoints.beyonder import beyonder_router
from app.api.endpoints.wiki import wiki_router
from app.api.endpoints.stats import stats_router
from app.api.endpoints.organ import organ_router
from app.api.endpoints.newspaper import news_paper_router
from app.api.endpoints.logs import logs_router
from app.service.main import MainService
from app.api.depends.session import get_session
from app.exception import get_exception_codes

base_router = APIRouter()

main_router = APIRouter(prefix='', tags=['main'], responses=get_exception_codes(types=[]))

@main_router.get('/info', response_model=AnswerBaseInfo)
async def get_info(
                   user_id: int = Query(description='ID пользователя'),
                   session = Depends(get_session())
                   ):
    return await MainService(session, purpose_user_id=user_id).info()

@main_router.put('/user/update', response_model=AnswerUserBody)
async def user_new(
                   query: QueryUserUpdate, 
                   session = Depends(get_session())
                   ):
    return await MainService(session).update(query)

@main_router.get('/user', response_model=AnswerUserBody)
async def user_telegram(
                   user_id: int = Query(None, description='ID пользователя'),
                   tg_id: int = Query(None, description='Telegram ID пользователя'),
                   session = Depends(get_session())
                   ):
    return await MainService(session, purpose_user_id=user_id).get_telegram(tg_id)

@main_router.get('/user/search', response_model=AnswerUsersBody)
async def user_search(
                   user_id: int | None = Query(None, description='ID пользователя'),
                   tg_id: int | None = Query(None, description='Telegram ID пользователя'),
                   username: str | None = Query(None, description='Telegram username'),
                   name: str | None = Query(None, description='Обычное имя пользователя'),
                   session = Depends(get_session())
                   ):
    return await MainService(session).search_users(user_id, tg_id, username, name)

@main_router.get('/user/list', response_model=AnswerUsersBody)
async def user_list(
                   session = Depends(get_session())
                   ):
    return await MainService(session).list_users()

@main_router.patch('/user/delete', response_model=AnswerUserBody)
async def user_delete(
                   query: QueryBody,
                   user_id: int = Query(description='ID пользователя'),
                   session = Depends(get_session())
                   ):
    return await MainService(
        session,
        user_id=query.user_id,
        is_admin=query.is_admin,
    ).delete_user(user_id)

base_router.include_router(main_router)
base_router.include_router(beyonder_router)
base_router.include_router(organ_router)
base_router.include_router(news_paper_router)
base_router.include_router(wiki_router)
base_router.include_router(stats_router)
base_router.include_router(logs_router)