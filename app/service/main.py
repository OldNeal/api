from app.logic.main import MainLogic
from app.service.base import BaseService

class MainService(BaseService):
    def __init__(self, session, tg_id):
        super().__init__(session, tg_id)
        self.logic = MainLogic(session, tg_id)

    async def info(self):
        return await self.logic.info()


