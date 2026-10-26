from fastapi import APIRouter, Depends, Query
from app.api.depends.session import get_session
from app.exception import get_exception_codes
from app.service.wiki import PathService
from app.validate.api.wiki import (
    AnswerAllGAInfo,
    AnswerAllGroupInfo,
    AnswerAllPathInfo,
    AnswerAllSeqInfo,
    AnswerGAFullInfo,
    AnswerGASearchInfo,
    AnswerGroupInfo,
    AnswerPathFullInfo,
    AnswerPathSearchInfo,
    AnswerSeqFullInfo,
    AnswerSeqSearchInfo,
)

wiki_router = APIRouter(prefix='/wiki', responses=get_exception_codes(types=['wiki']))

seq_router = APIRouter(prefix='/seq', tags=['seq'])
path_router = APIRouter(prefix='/path', tags=['path'])
ga_router = APIRouter(prefix='/ga', tags=['ga'])
group_router = APIRouter(prefix='/group', tags=['group'])


@seq_router.get('/search', response_model=AnswerSeqSearchInfo)
async def search_seq(
    value: str = Query(description='Запрос для поиска'),
    session=Depends(get_session()),
):
    return await PathService(session).seq_search(value)


@path_router.get('/search', response_model=AnswerPathSearchInfo)
async def search_path(
    value: str = Query(description='Запрос для поиска'),
    session=Depends(get_session()),
):
    return await PathService(session).search(value)


@ga_router.get('/search', response_model=AnswerGASearchInfo)
async def search_ga(
    value: str = Query(description='Запрос для поиска'),
    session=Depends(get_session()),
):
    return await PathService(session).ga_search(value)


@seq_router.get('/all', response_model=AnswerAllSeqInfo)
async def get_seqs(session=Depends(get_session())):
    return await PathService(session).seqs()


@path_router.get('/all', response_model=AnswerAllPathInfo)
async def get_paths(session=Depends(get_session())):
    return await PathService(session).paths()


@ga_router.get('/all', response_model=AnswerAllGAInfo)
async def get_gas(session=Depends(get_session())):
    return await PathService(session).gas()


@group_router.get('/all', response_model=AnswerAllGroupInfo)
async def get_groups(session=Depends(get_session())):
    return await PathService(session).groups()


@seq_router.get('', response_model=AnswerSeqFullInfo)
async def get_seq(
    name: str | None = Query(None, description='Навзание последовательности'),
    id: int | None = Query(None, description='ID последовательности'),
    session=Depends(get_session()),
):
    return await PathService(session).seq(name, id)


@path_router.get('', response_model=AnswerPathFullInfo)
async def get_path(
    name: str | None = Query(None, description='Навзание пути'),
    id: int | None = Query(None, description='ID пути'),
    session=Depends(get_session()),
):
    return await PathService(session).path(name, id)


@ga_router.get('', response_model=AnswerGAFullInfo)
async def get_ga(
    name: str | None = Query(None, description='Название Великого древнего'),
    id: int | None = Query(None, description='ID Великого древнего'),
    session=Depends(get_session()),
):
    return await PathService(session).ga(name, id)


@group_router.get('', response_model=AnswerGroupInfo)
async def get_group(
    name: str = Query(description='Название группы'),
    session=Depends(get_session()),
):
    return await PathService(session).group(name)


@path_router.get('/seq', response_model=AnswerSeqFullInfo)
async def get_seq_by_path_id(
    path_id: int = Query(description='ID пути'),
    seq_number: int = Query(description='Номер последовательности'),
    session=Depends(get_session()),
):
    return await PathService(session).seq_by_path_id(path_id, seq_number)


@path_router.get('/seqs', response_model=AnswerAllSeqInfo)
async def get_seqs_by_path_id(
    path_id: int = Query(description='ID пути'),
    session=Depends(get_session()),
):
    return await PathService(session).seqs_by_path_id(path_id)


@ga_router.get('/paths', response_model=AnswerAllPathInfo)
async def get_path_by_ga_id(
    ga_id: int = Query(description='ID Великого древнего'),
    session=Depends(get_session()),
):
    return await PathService(session).path_by_ga_id(ga_id)


wiki_router.include_router(seq_router)
wiki_router.include_router(path_router)
wiki_router.include_router(ga_router)
wiki_router.include_router(group_router)
