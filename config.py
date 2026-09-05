from dotenv import load_dotenv
import os
from pathlib import Path
from fastapi.routing import APIRoute

# Загружаем .env из корня проекта
load_dotenv(Path(__file__).parent / '.env')

class Settings:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')  
    
    TITLE = 'Old Neal Api'
    DESCRIPTION = 'API для Старого Нила'
    VERSION = os.getenv('VERSION')  
    DOCS = os.getenv('DOCS', 'f')   

    APP = os.getenv('APP', 'run:app')   
    HOST = os.getenv('HOST', '0.0.0.0')  
    PORT = int(os.getenv('PORT', 8000)) 
    RELOAD = os.getenv('RELOAD', 'f')  
    UVICORN_LOG_LEVEL = os.getenv('UVICORN_LOG_LEVEL', "WARNING")
    UVICORN_ACCESS_LOG = os.getenv('UVICORN_ACCESS_LOG', "f")
    
    ADMIN_TG_IDS = [int(id) for id in os.getenv('ADMIN_TG_IDS').split(',')]  

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    @property
    def admins(self):
        return self.ADMIN_TG_IDS

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


settings = Settings()
admins = settings.admins

def use_route_names_as_operation_ids(app) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name