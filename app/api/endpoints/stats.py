from fastapi import APIRouter, Depends
from app.validate.api.base import QueryBody, AnswerBaseInfo
from app.api.depends.session import get_session
from app.exception import get_exception_codes

stats_router = APIRouter(prefix='/stats', tags=['stats'])

@stats_router.get('/info')
async def endpoint(query: QueryBody, session = Depends(get_session())):
    pass
