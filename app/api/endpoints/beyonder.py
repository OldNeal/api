from fastapi import APIRouter, Depends
from app.validate.api.beyonder import QueryBody, AnswerInfoUpseq
from app.api.depends.session import get_session
from app.service.beyonder import BeyonderService

beyonder_router = APIRouter(prefix='/beyonder')

@beyonder_router.post('/drink/{path_name}')
async def endpoint(query: QueryBody, path_name: str, session = Depends(get_session())):
    data = await BeyonderService(session, query.tg_id).drink(path_name)
    return AnswerInfoUpseq.model_validate(data.model_dump() | {'tg_id':query.tg_id})
