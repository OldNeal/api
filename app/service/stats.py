from app.logic.stats import StatsLogic
from app.service.base import BaseService

class StatsService(BaseService):
    logic_cls: type[StatsLogic] = StatsLogic
    logic: StatsLogic

    async def all(self):
        return await self.logic.all()
    