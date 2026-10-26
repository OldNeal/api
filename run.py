from dark_swag import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exception.base import BaseException
from config import settings, use_route_names_as_operation_ids
from app.redis.base import lifespan, redis_ping
from app.redis.links import links, LinkHashs
import uvicorn, asyncio
from app.api.endpoints.main import base_router
from app.api.midlwares import LogMidlware
from app.exception import BaseExceptionResponse, get_exception_codes
from app.validate.api.base import AnswerMain
from app.logging.base import botlog
from app.db.metods.ping import ping_db

app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    responses=get_exception_codes(types=['base']),
    docs_url=settings.docs_url,     
    redoc_url=settings.redoc_url,    
    openapi_url=settings.openapi_url,
    lifespan=lifespan
)

app.include_router(base_router)
app.add_middleware(LogMidlware)

@app.get('/', response_model=AnswerMain)
def main():
    return AnswerMain(message=f'The Old Neal API, version: {app.version}', version=app.version)

@app.exception_handler(BaseException)
async def handle_base_error(request, exc: BaseException):
    return JSONResponse(status_code=exc.status_code, content=exc.content)

@app.exception_handler(HTTPException)
async def handle_value_error(request, exc: HTTPException):
    response = BaseExceptionResponse(message=exc.detail, status_code=exc.status_code, headers=exc.headers)
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())

@app.exception_handler(RequestValidationError)
async def handle_errors(request, exc):
    formatted_errors = [
        {
            "field": " -> ".join(str(loc) for loc in err["loc"]),
            "message": err["msg"],
            "type": err["type"]
        }
        for err in exc.errors()
    ]
    response = BaseExceptionResponse(message="Ошибка валидации входных данных", status_code=400, content=formatted_errors)

    return JSONResponse(status_code=response.status_code, content=response.model_dump())

@app.exception_handler(Exception)
async def handle_any_error(request, exc):
    response = BaseExceptionResponse(message='Unknown exception', status_code=500, headers={})
    return JSONResponse(status_code=response.status_code, content=response.model_dump())

use_route_names_as_operation_ids(app)

async def main():
    try:
        botlog.logger.info('API запускается')
        await ping_db(True)
        await redis_ping(True)
        await links.cache_all()
        await links.hscan_all(LinkHashs.TG_HASH)
        botlog.start()
        uvicorn.run(
            settings.APP, 
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.is_reload,
            log_level=settings.UVICORN_LOG_LEVEL,  
            access_log=settings.is_access_log
            ) 
    except:
        pass
    finally:
        botlog.stop()
    
if __name__ == '__main__':
    asyncio.run(main())
