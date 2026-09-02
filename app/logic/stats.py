from app.logic.base import BaseLogic
from app.validate.api.stats import AnswerAllStats
class StatsLogic(BaseLogic):
    async def all(self):
        return AnswerAllStats(
            users=await self.dao.user.count(),
            beyonders=await self.dao.beyonder.count(),
            members=await self.dao.member.count(),
            organs=await self.dao.organ.count(),
            paths=await self.dao.path.count(),
            gas=await self.dao.greatancient.count(),
        )