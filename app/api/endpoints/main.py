from fastapi import APIRouter, Depends, Query, Path
from app.validate.core import QueryBody, AnswerBaseInfo, QueryUserUpdate, AnswerUserBody, AnswerUsersBody
from app.api.endpoints.wiki import wiki_router
from app.api.endpoints.stats import stats_router
from app.exception import get_exception_codes

base_router = APIRouter()

base_router.include_router(wiki_router)
base_router.include_router(stats_router)