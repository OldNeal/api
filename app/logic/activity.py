from app.logic.item import ItemLogic


class ActivityLogic(ItemLogic):
    async def get_activity_points_count(self):
        user = await self.get_user(self.user_id)
        return await self._activity_points_answer(user, user)
