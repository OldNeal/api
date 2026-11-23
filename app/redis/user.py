from app.redis.base import BaseStore, BaseHashs

USER_UPDATE_TTL = 60 * 60 * 24

class UserHashs(BaseHashs):
    TOKEN_HASH = "token"
    USER_ID_HASH = "user_id"

class UserStore(BaseStore):
    hashs_cls = UserHashs
    hashs: type[UserHashs]
    
    async def get_user_id(self, token: str) -> int | None:
        v = await self.client.hget(self.hashs_cls.TOKEN_HASH, token)
        return int(v) if v else None
    
    async def get_token(self, user_id: int) -> int | None:
        v = await self.client.hget(self.hashs_cls.USER_ID_HASH, user_id)
        return v if v else None

    async def hscan_all(self, key: str, batch: int = 1000):
        cursor = 0
        cursor, chunk = await self.client.hscan(key, cursor=cursor, count=batch)
        return chunk
