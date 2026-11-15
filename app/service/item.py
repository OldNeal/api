from app.logic.item import ItemLogic
from app.service.base import BaseService


class ItemService(BaseService):
    def __init__(
        self,
        session,
        user_id: int | None = None,
        purpose_user_id: int | None = None,
        is_admin: bool = False,
    ):
        super().__init__(session, user_id, purpose_user_id, is_admin)
        self.logic = ItemLogic(
            session,
            user_id=user_id,
            purpose_user_id=purpose_user_id,
            is_admin=self.is_admin,
        )

    async def list_items(self, page: int | None = None, per_page: int = 5):
        return await self.logic.list_items(page, per_page)

    async def get_item(self, item_id: int):
        return await self.logic.get_item(item_id)

    async def get_inventory_item(self, item_id: int):
        return await self.logic.get_inventory_item(item_id)

    async def inventory(self, page: int | None = None, per_page: int = 5):
        return await self.logic.inventory(page, per_page)

    async def give(self, item_id: int, quantity: int):
        return await self.logic.give(item_id, quantity)

    async def take(self, item_id: int, quantity: int):
        return await self.logic.take(item_id, quantity)

    async def get_activity_points(self, message_count: int = 1):
        return await self.logic.get_activity_points(message_count)

    async def add_activity_points(
        self,
        purpose_user_id: int,
        points: int,
        reason: str | None = None,
    ):
        return await self.logic.add_activity_points(purpose_user_id, points, reason)

    async def deduct_activity_points(
        self,
        purpose_user_id: int,
        points: int,
        reason: str | None = None,
    ):
        return await self.logic.deduct_activity_points(purpose_user_id, points, reason)

    async def reset_activity_points(
        self,
        purpose_user_id: int,
        reason: str | None = None,
    ):
        return await self.logic.reset_activity_points(purpose_user_id, reason)

    async def reset_activity_points_limit(self, purpose_user_id: int):
        return await self.logic.reset_activity_points_limit(purpose_user_id)
