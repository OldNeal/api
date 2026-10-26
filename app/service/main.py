from app.logic.main import MainLogic
from app.service.base import BaseService

class MainService(BaseService):
    def __init__(self, session, user_id: int | None = None, purpose_user_id: int | None = None, is_admin: bool = False):
        super().__init__(session, user_id, purpose_user_id, is_admin)
        self.logic = MainLogic(session, user_id=user_id, purpose_user_id=purpose_user_id, is_admin=self.is_admin)

    async def info(self):
        return await self.logic.info()

    async def update(self, user):
        return await self.logic.update(user)
    
    async def get_telegram(self, tg_id: int | None = None):
        return await self.logic.get_telegram(tg_id)