from app.logic.activity import ActivityLogic
from app.validate.api.stats import AnswerAllStats

class StatsLogic(ActivityLogic):
    async def all(self):
        activity_point_sketch = await self._activity_point_sketch()
        return AnswerAllStats(
            users=await self.dao.user.count(),
            tg_users=await self.dao.tguser.count(),
            beyonders=await self.dao.beyonder.count(),
            members=await self.dao.member.count(),
            organs=await self.dao.organ.count(),
            paths=await self.dao.path.count(),
            gas=await self.dao.greatancient.count(),
            news_papers=await self.dao.news_paper.count(),
            questions=await self.dao.question.count(),
            activity_points_all_time=activity_point_sketch.all_counts_all_time
        )