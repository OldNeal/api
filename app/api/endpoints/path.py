from fastapi import APIRouter, Depends
from app.validate.api.path import AnswerBody, AnswerGAInfo, AnswerGroupInfo, AnswerPathInfo, AnswerGASearchInfo, AnswerPathSearchInfo
from app.service.path import PathService
from app.api.depends.session import get_session

path_router = APIRouter(prefix='/path')

@path_router.get('/{name}')
async def endpoint(name: str, session = Depends(get_session())):
    data = await PathService(session).path(name)
    return AnswerPathInfo.to_query(data)

@path_router.get('/ga/{name}')
async def endpoint(name: str, session = Depends(get_session())):
    data = await PathService(session).ga(name)
    return AnswerGAInfo.to_query(data)

@path_router.get('/group/{name}')
async def endpoint(name: str, session = Depends(get_session())):
    data = await PathService(session).group(name)
    return AnswerGroupInfo.to_query(data)

@path_router.get('/search/{value}')
async def endpoint(value: str, session = Depends(get_session())):
    data = await PathService(session).search(value)
    return AnswerPathSearchInfo.to_query(value, data)

@path_router.get('/ga/search/{value}')
async def endpoint(value: str, session = Depends(get_session())):
    data = await PathService(session).ga_search(value)
    return AnswerGASearchInfo.to_query(value, data)