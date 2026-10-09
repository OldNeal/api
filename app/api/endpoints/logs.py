from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import FileResponse
from app.validate.api.base import AnswerLogFileNames
from app.api.depends.session import get_session
from app.exception import get_exception_codes
from app.service.logs import LogsService

logs_router = APIRouter(prefix='/logs', tags=['logs'], responses=get_exception_codes(types=['logs']))

@logs_router.get('/file/get/{category}/{file_name}')
async def logs_file_get(        
                    category = Path(description='Категория  файла'),
                    file_name = Path(description='Названия файла')
                    ):
    data = await LogsService().get_file_by_name(category, file_name)
    return FileResponse(
        path=data,
        filename=data.name,
        media_type='text/plain'
    )

@logs_router.get('/file/names', response_model=AnswerLogFileNames)
async def logs_file_names(        
                    mask = Query(None, description='Маска файла'),
                    type = Query(None, description='Тип файла')
                    ):
    data = await LogsService().get_files(mask, type)
    return AnswerLogFileNames(names=list(map(str, data)))
