from fastapi import APIRouter
from app.api.endpoints.question import question_router
from app.exception import get_exception_codes

player_router = APIRouter(prefix='/player', responses=get_exception_codes(types=[]))
player_router.include_router(question_router)
