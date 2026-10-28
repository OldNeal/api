from app.redis.base import redis_client
from app.db.decor import get_dao, DAO

class LinkHashs:
    TG_HASH = "telegram_id"
    GENERAL_HASH = "general_id"

class RedisLinks:
    client = redis_client
    links = LinkHashs

    async def cache_user(self, user_id: int, tg_id: int | None = None):
        async with self.client.pipeline(transaction=True) as pipe:
            if tg_id: 
                pipe.hset(self.links.TG_HASH, tg_id, user_id)
                pipe.hset(self.links.GENERAL_HASH, user_id, tg_id)
            await pipe.execute()

    async def delete_user(self, user_id: int, tg_id: int | None = None):
        async with self.client.pipeline(transaction=True) as pipe:
            pipe.hdel(self.links.GENERAL_HASH, user_id)
            if tg_id is not None:
                pipe.hdel(self.links.TG_HASH, tg_id)
            await pipe.execute()

    @get_dao()
    async def cache_all(self, dao: DAO):
        users = await dao.user.find_all()
        async with self.client.pipeline(transaction=True) as pipe:
            for user in users: 
                pipe.hset(self.links.TG_HASH, user.tg_id, user.id)
                pipe.hset(self.links.GENERAL_HASH, user.id, user.tg_id)
            await pipe.execute()

    async def get_user_id(self, tg_id: int) -> int | None:
        v = await self.client.hget(self.links.TG_HASH, tg_id)
        return int(v) if v else None
    
    async def get_tg_id(self, user_id: int) -> int | None:
        v = await self.client.hget(self.links.GENERAL_HASH, user_id)
        return int(v) if v else None

    async def hscan_all(self, key: str, batch: int = 1000):
        cursor = 0
        cursor, chunk = await self.client.hscan(key, cursor=cursor, count=batch)
        return chunk

    async def delete_all(self, key: str):
        return bool(await self.client.delete(key))

    

links = RedisLinks()
