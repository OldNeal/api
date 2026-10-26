from app.logic.stats import StatsLogic
from app.service.base import BaseService

class StatsService(BaseService):
    def __init__(self, session, user_id: int | None = None, purpose_user_id: int | None = None, is_admin: bool = False):
        super().__init__(session, user_id, purpose_user_id, is_admin)
        self.logic = StatsLogic(session, user_id=user_id, purpose_user_id=purpose_user_id, is_admin=self.is_admin)

    async def all(self):
        return await self.logic.all()
    