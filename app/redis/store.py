from redis.asyncio import Redis
from app.redis.base import redis_client, redis_ping
from app.redis.user import UserStore
from app.redis.activity import ActivityStore
from app.redis.question import QuestionStore

class Store:
    def __init__(self, client: Redis = redis_client, **kwargs):
        self.client = client
        self.kwargs = kwargs

        self.user = UserStore(client, **kwargs)
        self.activity = ActivityStore(client, **kwargs)
        self.question = QuestionStore(client, **kwargs)

    @classmethod
    async def start(self):
        await self.ping()
        return await UserStore(redis_client).start()

    @classmethod
    async def ping(self):
        return await redis_ping(True)

    async def close(self):
        return await self.client.aclose()