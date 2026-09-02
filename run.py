from dark_swag import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exception.base import BaseException
from config import settings, use_route_names_as_operation_ids
import uvicorn
from app.api.endpoints.main import main_router
from app.api.midlwares import UpdateUserInfoMidlware
from app.exception import BaseExceptionResponse, get_exception_codes
from app.validate.api.base import AnswerMain
from app.logging.base import botlog

app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    description='API для Старого Нила',
    responses=get_exception_codes(types=['base'])
)

app.include_router(main_router)
app.add_middleware(UpdateUserInfoMidlware)

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

if __name__ == '__main__':
    botlog.start()
    uvicorn.run(
        "run:app", 
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level="WARNING",  
        access_log=False) 
