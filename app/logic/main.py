from app.logic.base import BaseLogic


class MainLogic(BaseLogic):
    async def info(self):
        user = await self.get_user()
        if user.beyonder:
            await user.beyonder.seq.path.awaitable_attrs.sequence_datas
        return user
