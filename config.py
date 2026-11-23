from dotenv import load_dotenv
import os
from pathlib import Path
from fastapi.routing import APIRoute

# Загружаем .env из корня проекта
load_dotenv(Path(__file__).parent / '.env')

class Settings:
    TITLE = 'Old Neal API'
    DESCRIPTION = 'API Старого Нила'
    VERSION = os.getenv('VERSION')  
    DOCS = os.getenv('DOCS', 'f')   
   
    CORE_URL = os.getenv('core_url')

    APP = os.getenv('APP', 'run:app')   
    HOST = os.getenv('HOST', '0.0.0.0')  
    PORT = int(os.getenv('PORT', 8080)) 
    RELOAD = os.getenv('RELOAD', 'f')  
    UVICORN_LOG_LEVEL = os.getenv('UVICORN_LOG_LEVEL', "WARNING")
    UVICORN_ACCESS_LOG = os.getenv('UVICORN_ACCESS_LOG', "f")
    
    ADMIN_USER_IDS = [int(id) for id in os.getenv('ADMIN_USER_IDS', '').split(',') if id]

    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')   
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

    VALUES = {}

    @property
    def admins(self):
        return self.ADMIN_USER_IDS

    @property
    def is_reload(self):
        return True if self.RELOAD == 't' else False
    
    @property
    def is_access_log(self):
        return True if self.UVICORN_ACCESS_LOG == 't' else False
    
    @property
    def docs_url(self):
        return '/docs' if self.DOCS == 't' else None

    @property
    def redoc_url(self):
        return '/redoc' if self.DOCS == 't' else None
    
    @property
    def openapi_url(self):
        return '/openapi.json' if self.DOCS == 't' else None

    @property
    def url(self):
        return f'http://localhost:{self.PORT}/'

settings = Settings()
admins = settings.admins

def use_route_names_as_operation_ids(app) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name

