from redis.asyncio import Redis
from app.redis.base import redis_client, redis_ping
from app.redis.user import UserStore

class Store:
    def __init__(self, client: Redis = redis_client, **kwargs):
        self.client = client
        self.kwargs = kwargs

        self.user = UserStore(client, **kwargs)

    @classmethod
    async def ping(self):
        return await redis_ping(True)

    async def close(self):
        return await self.client.aclose()

store = Store()