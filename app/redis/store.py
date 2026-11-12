from redis.asyncio import Redis
from app.redis.base import redis_client, redis_ping
from app.redis.user import UserStore
from app.redis.activity import ActivityStore

class Store:
    def __init__(self, client: Redis, **kwargs):
        self.client = client
        self.kwargs = kwargs

        self.user = UserStore(client, **kwargs)
        self.activity = ActivityStore(client, **kwargs)

    @classmethod
    async def start(self):
        await redis_ping(True)
        return await UserStore(redis_client).start()