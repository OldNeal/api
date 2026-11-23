from fastapi import APIRouter, Depends, Query, Request
from app.validate.core import QueryBody, AnswerBaseInfo, AnswerAllStats
from app.exception import get_exception_codes
from app.service.stats import StatsService

stats_router = APIRouter(prefix='/stats', tags=['stats'])

@stats_router.get('/all', response_model=AnswerAllStats)
async def stats_all(request: Request):
    return await StatsService(request_id=request.state.request_id).all()
