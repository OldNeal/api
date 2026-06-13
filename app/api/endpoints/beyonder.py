from fastapi import APIRouter, Depends, Query, Path
from app.validate.api.beyonder import (QueryBody, 
                                       AnswerTimeInfo, 
                                       AnswerTimeReplace, 
                                       AnswerTimeRedact, 
                                       AnswerRedactSeq,
                                       AnswerUserBody)
from app.api.depends.session import get_session
from app.service.beyonder import BeyonderService
from datetime import datetime, timedelta
from app.exception import get_exception_codes

beyonder_router = APIRouter(prefix='/beyonder', tags=['beyonder'], responses=get_exception_codes(types=['beyonder']))

@beyonder_router.put('/drink', response_model=AnswerRedactSeq)
async def drink(
                   query: QueryBody, 
                   tg_id: int = Query(None, description='Telegram ID пользователя'), 
                   path_name: str | None = Query(None, description='Название пути будущего потустороннего'), 
                   seq: int = Query(9, description='Последовательность указзаного пути'),
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session, query.tg_id, tg_id).drink(path_name, seq)
    return data

@beyonder_router.patch('/upseq', response_model=AnswerRedactSeq)
async def upseq(
                   query: QueryBody, 
                   tg_id: int = Query(None, description='Telegram ID пользователя'), 
                   path_name: str | None = Query(None, description='Путь на который переходит потусторонний, None - остаться на последовательности'), 
                   seq: int = Query(1, description='Насколько увеличить последовательнсоть?'),
                   session = Depends(get_session())
                   ):

    data = await BeyonderService(session, query.tg_id, tg_id).upseq(seq, path_name)
    return data

@beyonder_router.patch('/downseq', response_model=AnswerRedactSeq)
async def dowseq(
                   query: QueryBody, 
                   tg_id: int = Query(None, description='Telegram ID пользователя'), 
                   path_name: str | None = Query(None, description='Путь на который переходит потусторонний, None - остаться на последовательности'), 
                   seq: int = Query(1, description='Насколько понизить последовательнсоть'),
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session, query.tg_id, tg_id).downseq(seq, path_name)
    return data

@beyonder_router.get('/time/info/{tg_id}', response_model=AnswerTimeInfo)
async def time_info(
                   tg_id: int = Path(description='Telegram ID пользователя'), 
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session, tg_id).info()
    return data

@beyonder_router.patch('/time/replace', response_model=AnswerTimeReplace)
async def time_replace(
                   query: QueryBody, 
                   tg_id: int = Query(None, description='Telegram ID пользователя'), 
                   date: str = Query(description='Новая дата повышения последовательности'),
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session, query.tg_id, tg_id).replace_time(datetime.fromisoformat(date))
    return data

@beyonder_router.patch('/time/redact', response_model=AnswerTimeRedact)
async def time_redact(
                   query: QueryBody, 
                   tg_id: int = Query(None, description='Telegram ID пользователя'), 
                   seconds: float = Query(description='Кол-во секунд'), 
                   operator: str = Query(description='Что сделать с датой (+ или -)'), 
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session, query.tg_id, tg_id).edit_time(timedelta(seconds=seconds), operator)
    return data

@beyonder_router.delete('/kill', response_model=AnswerUserBody)
async def kill(
                   query: QueryBody, 
                   tg_id: int = Query(None, description='Telegram ID пользователя'), 
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session, query.tg_id, tg_id).kill()
    return AnswerUserBody(tg_id=tg_id)

