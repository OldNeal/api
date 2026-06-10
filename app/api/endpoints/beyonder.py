from fastapi import APIRouter, Depends
from app.validate.api.base import QueryBody, QueryInfo

beyonder_router = APIRouter(prefix='/beyonder')

@beyonder_router.get('/info')
async def api_get_sketchs(query: QueryBody):
    pass
