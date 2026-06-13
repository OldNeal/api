from fastapi import APIRouter, Depends, Query, Path
from app.validate.api.path import (
                                   AnswerBody, 
                                   AnswerGAFullInfo, 
                                   AnswerGroupInfo, 
                                   AnswerPathFullInfo, 
                                   AnswerGASearchInfo, 
                                   AnswerPathSearchInfo, 
                                   AnswerSeqSearchInfo,
                                   AnswerAllGAInfo,
                                   AnswerAllPathInfo,
                                   AnswerAllSeqInfo,
                                   AnswerAllGroupInfo
                                   )
from app.service.path import PathService
from app.api.depends.session import get_session
from app.exception import get_exception_codes

wiki_router = APIRouter(prefix='/wiki', responses=get_exception_codes(types=['wiki']))

seq_router = APIRouter(prefix='/seq', tags=['seq'])
path_router = APIRouter(prefix='/path', tags=['path'])
ga_router = APIRouter(prefix='/ga', tags=['ga'])
group_router = APIRouter(prefix='/group', tags=['group'])

@seq_router.get('/search', response_model=AnswerSeqSearchInfo)
async def search_seq(
                      value: str = Query(description='Запрос для поиска'), 
                      session = Depends(get_session())
                      ):
    data = await PathService(session).search(value)
    return AnswerSeqSearchInfo.to_query(value, data)

@path_router.get('/search', response_model=AnswerPathSearchInfo)
async def search_path(
                      value: str = Query(description='Запрос для поиска'), 
                      session = Depends(get_session())
                      ):
    data = await PathService(session).search(value)
    return AnswerPathSearchInfo.to_query(value, data)

@ga_router.get('/search', response_model=AnswerGASearchInfo)
async def search_ga(
                    value: str = Query(description='Запрос для поиска'), 
                    session = Depends(get_session())
                    ):
    data = await PathService(session).ga_search(value)
    return AnswerGASearchInfo.to_query(value, data)






@seq_router.get('/all', response_model=AnswerAllSeqInfo)
async def get_seqs(session = Depends(get_session())):
    data = await PathService(session).seqs()
    return AnswerAllSeqInfo.to_query(data)

@path_router.get('/all', response_model=AnswerAllPathInfo)
async def get_paths(session = Depends(get_session())):
    data = await PathService(session).paths()
    return AnswerPathFullInfo.to_query(data)

@ga_router.get('/all', response_model=AnswerAllGAInfo)
async def get_gas(session = Depends(get_session())):
    data = await PathService(session).gas()
    return AnswerGAFullInfo.to_query(data)

@group_router.get('/all', response_model=AnswerAllGroupInfo)
async def get_groups(session = Depends(get_session())):
    data = await PathService(session).groups()
    return AnswerAllGroupInfo(groups=data)






@path_router.get('', response_model=AnswerPathFullInfo)
async def get_path(
                          name: str = Query(None, description='Навзание пути'), 
                          id: int = Query(None, description='ID пути'), 
                          session = Depends(get_session())
                          ):
    data = await PathService(session).path(name, id)
    return AnswerPathFullInfo.to_query(data)

@ga_router.get('', response_model=AnswerGAFullInfo)
async def get_ga(
                         name: str = Query(None, description='Название Великого древнего'),
                         id: int = Query(None, description='ID Великого древнего'),  
                         session = Depends(get_session())
                         ):
    data = await PathService(session).ga(name, id)
    return AnswerGAFullInfo.to_query(data)

@group_router.get('', response_model=AnswerGroupInfo)
async def get_group(
                            name: str = Query(description='Название группы'), 
                            session = Depends(get_session())
                            ):
    data = await PathService(session).group(name)
    return AnswerGroupInfo.to_query(data)




wiki_router.include_router(seq_router)
wiki_router.include_router(path_router)
wiki_router.include_router(ga_router)
wiki_router.include_router(group_router)
