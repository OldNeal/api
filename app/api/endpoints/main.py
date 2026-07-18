from fastapi import APIRouter, Depends, Query, Path
from app.validate.api.base import QueryBody, AnswerBaseInfo
from app.api.endpoints.beyonder import beyonder_router
from app.api.endpoints.path import wiki_router
from app.api.endpoints.stats import stats_router
from app.service.main import MainService
from app.api.depends.session import get_session
from app.exception import get_exception_codes

main_router = APIRouter()
main_router.include_router(beyonder_router)
main_router.include_router(wiki_router)
main_router.include_router(stats_router)

@main_router.get('/info/{tg_id}', tags=['main'], operation_id='get_info', response_model=AnswerBaseInfo)
async def get_info(
                   tg_id: int = Path(description='Telegram ID пользователя'), 
                   session = Depends(get_session())
                   ):
    data = await MainService(session, tg_id).info()
    return data

