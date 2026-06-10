from fastapi import APIRouter, Depends
from app.validate.api.base import QueryBody, QueryInfo
from app.api.endpoints.beyonder import beyonder_router
from app.service.main import MainService
from app.api.depends.session import get_session

main_router = APIRouter(prefix='/main')
main_router.include_router(beyonder_router)

@main_router.get('/info/{tg_id}')
async def api_get_sketchs(tg_id: int, session = Depends(get_session())):
    print(session.is_active)
    user = await MainService(session, tg_id).info()
    print(session.is_active)
    return QueryInfo(tg_id=tg_id).to_query(user)
