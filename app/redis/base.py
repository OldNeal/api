from config import settings
from contextlib import asynccontextmanager
import redis.asyncio as redis
from dark_swag import FastAPI
from datetime import datetime
from app.logging.base import botlog
from app.exception.base import RedisError

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

async def redis_ping(logged: bool = False):
            try:
                start = datetime.now()
                response = await redis_client.ping()
                if response:
                    end = datetime.now()
                    result = f'{int((end - start).total_seconds()*1000)}'
                    if logged:
                        botlog.logger.info('Redis работает', ping=result)
                    return result
                raise RedisError()
            except Exception as e:
                raise RedisError(error=str(e))

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()