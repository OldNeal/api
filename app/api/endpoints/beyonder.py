from fastapi import APIRouter, Depends, Query, Path
from app.validate.api.beyonder import (QueryBody, 
                                       AnswerTimeInfo, 
                                       AnswerTimeReplace, 
                                       AnswerTimeRedact, 
                                       AnswerRedactSeq,
                                       AnswerBody,
                                       AnswerBeyonderInfo,
                                       AnswerBeyonderList)
from app.api.depends.session import get_session
from app.service.beyonder import BeyonderService
from datetime import datetime, timedelta
from app.exception import get_exception_codes

beyonder_router = APIRouter(prefix='/beyonder', tags=['beyonder'], responses=get_exception_codes(types=['beyonder', 'wiki']))

@beyonder_router.get('/info', response_model=AnswerBeyonderInfo)
async def beyonder_info(
                user_id: int = Query(description='ID пользователя'),
                session = Depends(get_session())
                ):
    return await BeyonderService(session, purpose_user_id=user_id).info()

@beyonder_router.put('/drink', response_model=AnswerRedactSeq)
async def beyonder_drink(
                query: QueryBody, 
                user_id: int = Query(None, description='ID пользователя'),
                path_name: str | None = Query(None, description='Название пути будущего потустороннего'), 
                path_id: int | None = Query(None, description='ID пути будущего потустороннего'), 
                seq: int = Query(9, description='Последовательность указзаного пути'),
                session = Depends(get_session())
                ):
    return await BeyonderService(session, query.user_id, user_id, query.is_admin).drink(path_name, path_id, seq)

@beyonder_router.patch('/upseq', response_model=AnswerRedactSeq)
async def beyonder_upseq(
                query: QueryBody, 
                user_id: int = Query(None, description='ID пользователя'),
                path_name: str | None = Query(None, description='Путь на который переходит потусторонний, None - остаться на последовательности'), 
                seq: int = Query(None, description='Новая последовательность'),
                session = Depends(get_session())
                ):
    return await BeyonderService(session, query.user_id, user_id, query.is_admin).upseq(seq, path_name)

@beyonder_router.patch('/downseq', response_model=AnswerRedactSeq)
async def beyonder_dowseq(
                 query: QueryBody, 
                 user_id: int = Query(None, description='ID пользователя'),
                 path_name: str | None = Query(None, description='Путь на который переходит потусторонний, None - остаться на последовательности'), 
                 seq: int = Query(None, description='Новая последовательность'),
                 session = Depends(get_session())
                 ):
    return await BeyonderService(session, query.user_id, user_id, query.is_admin).downseq(seq, path_name)

@beyonder_router.get('/time/info', response_model=AnswerTimeInfo)
async def beyonder_time_info(
                   user_id: int = Query(description='ID пользователя'),
                   to_raise: bool = Query(False, description='Вызывать ли исключение'),
                   session = Depends(get_session())
                   ):
    return await BeyonderService(session, user_id).time_info(to_raise)

@beyonder_router.patch('/time/replace', response_model=AnswerTimeReplace)
async def beyonder_time_replace(
                   query: QueryBody, 
                   user_id: int = Query(None, description='ID пользователя'),
                   date: str = Query(description='Новая дата повышения последовательности'),
                   session = Depends(get_session())
                   ):
    return await BeyonderService(session, query.user_id, user_id, query.is_admin).replace_time(datetime.fromisoformat(date))

@beyonder_router.patch('/time/redact', response_model=AnswerTimeRedact)
async def beyonder_time_redact(
                   query: QueryBody, 
                   user_id: int = Query(None, description='ID пользователя'),
                   seconds: float = Query(description='Кол-во секунд'), 
                   operator: str = Query(description='Что сделать с датой (+ или -)'), 
                   session = Depends(get_session())
                   ):
    return await BeyonderService(session, query.user_id, user_id, query.is_admin).edit_time(timedelta(seconds=seconds), operator)

@beyonder_router.post('/kill', response_model=AnswerBody)
async def beyonder_kill(
                   query: QueryBody, 
                   user_id: int = Query(None, description='ID пользователя'),
                   session = Depends(get_session())
                   ):
    return await BeyonderService(session, query.user_id, user_id, query.is_admin).kill()

@beyonder_router.get('/list', response_model=AnswerBeyonderList)
async def beyonder_list(
                   path_id: int = Query(description='ID Пути'),
                   session = Depends(get_session())
                   ):
    return await BeyonderService(session).list(path_id)