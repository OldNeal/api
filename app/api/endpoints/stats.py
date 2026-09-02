from fastapi import APIRouter, Depends, Query
from app.validate.api.base import QueryBody, AnswerBaseInfo
from app.api.depends.session import get_session
from app.exception import get_exception_codes
from app.service.stats import StatsService
from app.validate.api.stats import AnswerAllStats

stats_router = APIRouter(prefix='/stats', tags=['stats'])

@stats_router.get('/all', tags=['stats'], operation_id='stats_all', response_model=AnswerAllStats)
async def stats_all(              
                     session = Depends(get_session())
                     ):
    data = await StatsService(session).all()
    return data
