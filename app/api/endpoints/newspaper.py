from fastapi import APIRouter, Depends, Query

from app.api.depends.session import get_session
from app.exception import get_exception_codes
from app.service.newspaper import NewsPaperService
from app.validate.api.base import QueryBody
from app.validate.api.newspaper import (
    AnswerAllNewsPaperInfo,
    AnswerNewsPaperInfo,
    AnswerNewsPaperInfoDescription,
    AnswerReaderInfo,
    AnswerNewsPaperInfoReaders,
    AnswerRedactRank,
    AnswerNewsPaperSetting,
    AnswerNewsPaperSettingValues,
    AnswerNewsPaperGive,
    QueryNewsPaperSetting,
    QueryNewsPaperSettingDefault,
)

news_paper_router = APIRouter(
    prefix="/newspaper",
    tags=["newspaper"],
    responses=get_exception_codes(types=["newspaper", "setting"]),
)

@news_paper_router.get("/search", response_model=AnswerAllNewsPaperInfo)
async def news_paper_search(
    name: str = Query(description="Название газеты"),
    session = Depends(get_session()),
):
    return await NewsPaperService(session).search(name)


@news_paper_router.post("/all", response_model=AnswerAllNewsPaperInfo)
async def news_paper_all(
    query: QueryBody,
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id).all()

@news_paper_router.post("/list", response_model=AnswerAllNewsPaperInfo)
async def news_paper_list(
    query: QueryBody,
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id).news_papers()

@news_paper_router.post("/editors", response_model=AnswerAllNewsPaperInfo)
async def news_paper_list_where_editor(
    query: QueryBody,
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id).news_papers_where_editor()

@news_paper_router.post("/for_subscribe", response_model=AnswerAllNewsPaperInfo)
async def news_paper_for_subscribe(
    query: QueryBody,
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id).news_papers_for_subscribe()

@news_paper_router.post("/info", response_model=AnswerNewsPaperInfo)
async def news_paper_info(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).info()

@news_paper_router.post("/info/description", response_model=AnswerNewsPaperInfoDescription)
async def news_paper_info_description(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    session = Depends(get_session()),
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).description()


@news_paper_router.post("/readers", response_model=AnswerNewsPaperInfoReaders)
async def news_paper_readers(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).readers()

@news_paper_router.post("/reader", response_model=AnswerReaderInfo)
async def news_paper_reader(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    tg_id: int | None = Query(None, description="ID читателя"),
    session = Depends(get_session())
):
    return await NewsPaperService(
        session,
        query.tg_id,
        purpose_tg_id=tg_id,
        news_paper_id=id,
    ).reader()


@news_paper_router.put("/create", response_model=AnswerNewsPaperInfo)
async def news_paper_create(
    query: QueryBody,
    name: str = Query(description="Название новой газеты"),
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id).create(name)


@news_paper_router.put("/subscribe", response_model=AnswerNewsPaperInfo)
async def news_paper_subscribe(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).subscribe()


@news_paper_router.patch("/unsubscribe", response_model=AnswerNewsPaperInfo)
async def news_paper_unsubscribe(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).unsubscribe()


@news_paper_router.post("/notify", response_model=AnswerNewsPaperInfoReaders)
async def news_paper_notify(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).notify()


@news_paper_router.patch("/editor/make", response_model=AnswerRedactRank)
async def news_paper_make_editor(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    tg_id: int = Query(description="Telegram ID пользователя"),
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id, purpose_tg_id=tg_id, news_paper_id=id).make_editor()


@news_paper_router.patch("/editor/fire", response_model=AnswerRedactRank)
async def news_paper_fire_editor(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    tg_id: int = Query(description="Telegram ID пользователя"),
    session = Depends(get_session())
):
    return await NewsPaperService(session, query.tg_id, purpose_tg_id=tg_id, news_paper_id=id).fire_editor()

@news_paper_router.post("/capture", response_model=AnswerNewsPaperInfo)
async def news_paper_capture(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    session=Depends(get_session()),
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).capture()


@news_paper_router.post("/give", response_model=AnswerNewsPaperGive)
async def news_paper_give(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    tg_id: int = Query(description="Telegram ID пользователя"),
    session=Depends(get_session()),
):
    return await NewsPaperService(
        session,
        query.tg_id,
        purpose_tg_id=tg_id,
        news_paper_id=id,
    ).give()


@news_paper_router.post("/settings", response_model=AnswerNewsPaperSetting)
async def news_paper_settings(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    session=Depends(get_session()),
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).settings()


@news_paper_router.post("/settings/values", response_model=AnswerNewsPaperSettingValues)
async def news_paper_settings_values(
    query: QueryBody,
    id: int = Query(description="ID газеты"),
    session=Depends(get_session()),
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).settings_values()


@news_paper_router.patch("/settings/redact", response_model=AnswerNewsPaperSetting)
async def news_paper_settings_redact(
    query: QueryNewsPaperSetting,
    id: int = Query(description="ID газеты"),
    session=Depends(get_session()),
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).settings_redact(query.parametrs)


@news_paper_router.patch("/settings/default", response_model=AnswerNewsPaperSetting)
async def news_paper_settings_default(
    query: QueryNewsPaperSettingDefault,
    id: int = Query(description="ID газеты"),
    session=Depends(get_session()),
):
    return await NewsPaperService(session, query.tg_id, news_paper_id=id).settings_default(query.to_default)
