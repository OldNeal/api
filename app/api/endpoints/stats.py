from fastapi import APIRouter, Depends
from app.validate.api.base import QueryBody, AnswerBaseInfo
from app.api.depends.session import get_session

stats_router = APIRouter(prefix='/stats')

@stats_router.get('/info')
async def endpoint(query: QueryBody, session = Depends(get_session())):
    pass
