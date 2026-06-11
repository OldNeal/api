from fastapi import APIRouter, Depends
from app.validate.api.base import QueryBody, AnswerBaseInfo
from app.api.endpoints.beyonder import beyonder_router
from app.api.endpoints.path import path_router
from app.api.endpoints.stats import stats_router
from app.service.main import MainService
from app.api.depends.session import get_session

main_router = APIRouter()
main_router.include_router(beyonder_router)
main_router.include_router(path_router)
main_router.include_router(stats_router)

@main_router.get('/info/{tg_id}')
async def endpoint(tg_id: int, session = Depends(get_session())):
    user = await MainService(session, tg_id).info()
    return AnswerBaseInfo(tg_id=tg_id).to_query(user)
