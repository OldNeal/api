from config import settings
from contextlib import asynccontextmanager
from redis.asyncio import Redis
from dark_swag import FastAPI
from datetime import datetime
from app.logging.base import botlog
from app.exception.base import RedisError

redis_client = Redis(
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

class BaseHashs:
    pass

class BaseStore:
    hashs_cls = BaseHashs
    hashs: type[BaseHashs]

    def __init__(self, client: Redis, **kwargs):
        self.client = client
        self.kwargs = kwargs

        self.hashs = self.hashs_cls
