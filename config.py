from dotenv import load_dotenv
import os
from pathlib import Path

# Загружаем .env из корня проекта
load_dotenv(Path(__file__).parent / '.env')

class Settings:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')  
    TITLE = 'Old Neal Api'
    VERSION = '0.1'
    
    ADMIN_TG_IDS = [int(id) for id in os.getenv('ADMIN_TG_IDS').split(',')]  

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    @property
    def admins(self):
        return self.ADMIN_TG_IDS

settings = Settings()
admins = settings.admins