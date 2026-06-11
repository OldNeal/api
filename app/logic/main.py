from app.logic.base import BaseLogic


class MainLogic(BaseLogic):
    async def info(self):
        return await self.get_user()
