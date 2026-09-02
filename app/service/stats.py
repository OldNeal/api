from app.logic.stats import StatsLogic
from app.service.base import BaseService

class StatsService(BaseService):
    def __init__(self, session, tg_id: int | None = None, purpose_tg_id: int | None = None, is_admin: bool = False):
        super().__init__(session, tg_id, purpose_tg_id, is_admin)
        self.logic = StatsLogic(session, tg_id=tg_id, purpose_tg_id=purpose_tg_id, is_admin=self.is_admin)

    async def all(self):
        return await self.logic.all()
    