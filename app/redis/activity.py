from app.redis.base import BaseStore, BaseHashs
from app.exception.activity import ActivityPointLimitError

class ActivityHashs(BaseHashs):
    GET_POINTS = 'act:get-points:{user_id}'

    @classmethod
    def get_points(self, user_id: int):
        return self.GET_POINTS.format(user_id=user_id)

class ActivityStore(BaseStore):
    hashs_cls = ActivityHashs
    hashs: type[ActivityHashs]

    async def reset_activity_points_limit(self, user_id: int):
        return await self.client.delete(self.hashs.get_points(user_id))

    async def get_activity_points_limit(self, user_id: int):
        key = self.hashs.get_points(user_id)
        count = await self.client.get(key)
        ttl = await self.client.pttl(key)
        return int(count) if count else 0, max(0, ttl // 1000) if ttl >= 0 else 0
    
    async def check_activity_points(self, user_id: int, activity_points: int, activity_point_limit_ttl: int = 0, activity_points_limit: int = 0):
        key = self.hashs.get_points(user_id)
        existed = await self.client.exists(key)
        activity_points = await self.client.incr(key, activity_points)
        if not existed and activity_point_limit_ttl > 0:
            await self.client.expire(key, activity_point_limit_ttl)
        if activity_points > activity_points_limit:
            raise ActivityPointLimitError()
        return activity_points
