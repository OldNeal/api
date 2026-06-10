from fastapi import FastAPI
from config import settings
import uvicorn
from app.api.endpoints.main import main_router

app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
)

app.include_router(main_router)

@app.get('/')
def main():
    return f'The Old Neal API, version: {app.version}'

if __name__ == '__main__':
    uvicorn.run("run:app", reload=True)