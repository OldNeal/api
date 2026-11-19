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
    
    async def check_activity_points(self, user_id: int, activity_points: int, activity_point_limit_ttl: int = 0, activity_points_limit: int = 0):
        key = self.hashs.get_points(user_id)
        activity_points = await self.client.incr(key, activity_points)
        if await self.client.exists(key) == 0 and activity_point_limit_ttl > 0:
            await self.client.expire(key, activity_point_limit_ttl)
        if activity_points > activity_points_limit:
            raise ActivityPointLimitError()
        return activity_points
