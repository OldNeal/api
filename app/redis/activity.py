from app.redis.base import BaseStore, BaseHashs
from app.exception.activity import ActivityPointLimitError

GET_ACTIVITY_POINTS_TTL = 60*60*60
GET_ACTIVITY_POINTS_LIMIT = 200

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
    
    async def check_activity_points(self, user_id: int, activity_points: int):
        key = self.hashs.get_points(user_id)
        if await self.client.exists(key) == 0:
            activity_points = await self.client.incr(key, activity_points)
            await self.client.expire(key, GET_ACTIVITY_POINTS_TTL)
        else:
            activity_points = await self.client.incr(key, activity_points)
        if activity_points > GET_ACTIVITY_POINTS_LIMIT:
            raise ActivityPointLimitError()
        return activity_points
