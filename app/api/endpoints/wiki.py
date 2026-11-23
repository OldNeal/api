from fastapi import APIRouter, Depends, Query, Request
from app.exception import get_exception_codes
from app.service.wiki import WikiService
from app.validate.core import (
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
    request: Request,
    value: str = Query(description='Запрос для поиска'),
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
):
    return await WikiService(request_id=request.state.request_id).seq_search(value, page, per_page)


@path_router.get('/search', response_model=AnswerPathSearchInfo)
async def search_path(
    request: Request,
    value: str = Query(description='Запрос для поиска'),
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
):
    return await WikiService(request_id=request.state.request_id).path_search(value, page, per_page)


@ga_router.get('/search', response_model=AnswerGASearchInfo)
async def search_ga(
    request: Request,
    value: str = Query(description='Запрос для поиска'),
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
):
    return await WikiService(request_id=request.state.request_id).ga_search(value, page, per_page)


@seq_router.get('/all', response_model=AnswerAllSeqInfo)
async def get_seqs(
    request: Request,
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
):
    return await WikiService(request_id=request.state.request_id).seqs(page, per_page)


@path_router.get('/all', response_model=AnswerAllPathInfo)
async def get_paths(
    request: Request,
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
):
    return await WikiService(request_id=request.state.request_id).paths(page, per_page)


@ga_router.get('/all', response_model=AnswerAllGAInfo)
async def get_gas(
    request: Request,
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
):
    return await WikiService(request_id=request.state.request_id).gas(page, per_page)


@group_router.get('/all', response_model=AnswerAllGroupInfo)
async def get_groups(
    request: Request,
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
):
    return await WikiService(request_id=request.state.request_id).groups(page, per_page)


@seq_router.get('', response_model=AnswerSeqFullInfo)
async def get_seq(
    request: Request,
    name: str | None = Query(None, description='Навзание последовательности'),
    id: int | None = Query(None, description='ID последовательности'),
):
    return await WikiService(request_id=request.state.request_id).seq(name, id)


@path_router.get('', response_model=AnswerPathFullInfo)
async def get_path(
    request: Request,
    name: str | None = Query(None, description='Навзание пути'),
    id: int | None = Query(None, description='ID пути'),
):
    return await WikiService(request_id=request.state.request_id).path(name, id)


@ga_router.get('', response_model=AnswerGAFullInfo)
async def get_ga(
    request: Request,
    name: str | None = Query(None, description='Название Великого древнего'),
    id: int | None = Query(None, description='ID Великого древнего'),
):
    return await WikiService(request_id=request.state.request_id).ga(name, id)


@group_router.get('', response_model=AnswerGroupInfo)
async def get_group(
    request: Request,
    name: str = Query(description='Название группы'),
):
    return await WikiService(request_id=request.state.request_id).group(name)


@path_router.get('/seq', response_model=AnswerSeqFullInfo)
async def get_seq_by_path_id(
    request: Request,
    path_id: int = Query(description='ID пути'),
    seq_number: int = Query(description='Номер последовательности'),
):
    return await WikiService(request_id=request.state.request_id).seq_by_path_id(path_id, seq_number)


@path_router.get('/seqs', response_model=AnswerAllSeqInfo)
async def get_seqs_by_path_id(
    request: Request,
    path_id: int = Query(description='ID пути'),
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
):
    return await WikiService(request_id=request.state.request_id).seqs_by_path_id(path_id, page, per_page)


@ga_router.get('/paths', response_model=AnswerAllPathInfo)
async def get_path_by_ga_id(
    request: Request,
    ga_id: int = Query(description='ID Великого древнего'),
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
):
    return await WikiService(request_id=request.state.request_id).path_by_ga_id(ga_id, page, per_page)


wiki_router.include_router(seq_router)
wiki_router.include_router(path_router)
wiki_router.include_router(ga_router)
wiki_router.include_router(group_router)
