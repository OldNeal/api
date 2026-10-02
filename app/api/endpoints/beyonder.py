from fastapi import APIRouter, Depends, Query, Path
from app.validate.api.beyonder import (QueryBody, 
                                       AnswerTimeInfo, 
                                       AnswerTimeReplace, 
                                       AnswerTimeRedact, 
                                       AnswerRedactSeq,
                                       AnswerUserBody,
                                       AnswerBeyonderInfo,
                                       AnswerBeyonderList)
from app.api.depends.session import get_session
from app.service.beyonder import BeyonderService
from datetime import datetime, timedelta
from app.exception import get_exception_codes

beyonder_router = APIRouter(prefix='/beyonder', tags=['beyonder'], responses=get_exception_codes(types=['beyonder', 'wiki']))

@beyonder_router.get('/info', response_model=AnswerBeyonderInfo)
async def beyonder_info(
                tg_id: int = Query(description='Telegram ID пользователя'), 
                session = Depends(get_session())
                ):
    data = await BeyonderService(session, purpose_tg_id=tg_id).info()
    return data

@beyonder_router.put('/drink', response_model=AnswerRedactSeq)
async def beyonder_drink(
                query: QueryBody, 
                tg_id: int = Query(None, description='Telegram ID пользователя'), 
                path_name: str | None = Query(None, description='Название пути будущего потустороннего'), 
                path_id: int | None = Query(None, description='ID пути будущего потустороннего'), 
                seq: int = Query(9, description='Последовательность указзаного пути'),
                session = Depends(get_session())
                ):
    data = await BeyonderService(session, query.tg_id, tg_id, query.is_admin).drink(path_name, path_id, seq)
    return data

@beyonder_router.patch('/upseq', response_model=AnswerRedactSeq)
async def beyonder_upseq(
                query: QueryBody, 
                tg_id: int = Query(None, description='Telegram ID пользователя'), 
                path_name: str | None = Query(None, description='Путь на который переходит потусторонний, None - остаться на последовательности'), 
                seq: int = Query(None, description='Новая последовательность'),
                session = Depends(get_session())
                ):
    data = await BeyonderService(session, query.tg_id, tg_id, query.is_admin).upseq(seq, path_name)
    return data

@beyonder_router.patch('/downseq', response_model=AnswerRedactSeq)
async def beyonder_dowseq(
                 query: QueryBody, 
                 tg_id: int = Query(None, description='Telegram ID пользователя'), 
                 path_name: str | None = Query(None, description='Путь на который переходит потусторонний, None - остаться на последовательности'), 
                 seq: int = Query(None, description='Новая последовательность'),
                 session = Depends(get_session())
                 ):
    data = await BeyonderService(session, query.tg_id, tg_id, query.is_admin).downseq(seq, path_name)
    return data

@beyonder_router.get('/time/info/{tg_id}', response_model=AnswerTimeInfo)
async def beyonder_time_info(
                   tg_id: int = Path(description='Telegram ID пользователя'), 
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session, tg_id).time_info()
    return data

@beyonder_router.patch('/time/replace', response_model=AnswerTimeReplace)
async def beyonder_time_replace(
                   query: QueryBody, 
                   tg_id: int = Query(None, description='Telegram ID пользователя'), 
                   date: str = Query(description='Новая дата повышения последовательности'),
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session, query.tg_id, tg_id, query.is_admin).replace_time(datetime.fromisoformat(date))
    return data

@beyonder_router.patch('/time/redact', response_model=AnswerTimeRedact)
async def beyonder_time_redact(
                   query: QueryBody, 
                   tg_id: int = Query(None, description='Telegram ID пользователя'), 
                   seconds: float = Query(description='Кол-во секунд'), 
                   operator: str = Query(description='Что сделать с датой (+ или -)'), 
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session, query.tg_id, tg_id, query.is_admin).edit_time(timedelta(seconds=seconds), operator)
    return data

@beyonder_router.post('/kill', response_model=AnswerUserBody)
async def beyonder_kill(
                   query: QueryBody, 
                   tg_id: int = Query(None, description='Telegram ID пользователя'), 
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session, query.tg_id, tg_id, query.is_admin).kill()
    return data

@beyonder_router.get('/list', response_model=AnswerBeyonderList)
async def beyonder_list(
                   path_id: int = Query(description='ID Пути'),
                   session = Depends(get_session())
                   ):
    data = await BeyonderService(session).list(path_id)
    return data