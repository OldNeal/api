from app.db.models.item import InventoryDB, ItemDB, ItemSketchDB
from app.exception.item import ItemDontFindException, ItemQuantityException
from config import settings
from app.validate.api.base import AnswerActivityPoints
from app.logic.item import ItemLogic

ACTIVITY_POINTS_TAG = 'activity_point'
ACTIVITY_POINTS_MESSAGE = 10
GET_ACTIVITY_POINTS_LIMIT_TTL_MESSAGE = 60*60*60*24
GET_ACTIVITY_POINTS_LIMIT_MESSAGE = 1200
ACTIVITY_POINTS_QUESTION = 150


class ActivityLogic(ItemLogic):

    async def _activity_point_sketch(self):
        sketch = await self.dao.item_sketch.query_by_tag(ACTIVITY_POINTS_TAG)
        if sketch is None:
            raise ItemDontFindException()
        return sketch

    async def _activity_point_item(self, user, create: bool = False):
        sketch = await self._activity_point_sketch()
        inventory = user.inventory
        if inventory is None and create:
            inventory = InventoryDB()
            user.inventory = inventory
            await self.dao.flush()
        item = (
            await self.dao.item.query_by_inventory_and_sketch(inventory.id, sketch.id)
            if inventory is not None
            else None
        )
        return sketch, inventory, item

    async def _activity_points_answer(self, admin, target, points: int = 0):
        _, _, item = await self._activity_point_item(target)
        return AnswerActivityPoints(
            user=self.return_query_body(admin),
            purpose=self.return_query_body(target),
            activity_points=item.quantity if item else 0,
            get_activity_points=points,
        )

    async def get_activity_points(self, user, points: int):
        sketch, inventory, item = await self._activity_point_item(user, create=True)
        if item is None:
            item = ItemDB(
                sketch_id=sketch.id,
                inventory_id=inventory.id,
                quantity=points,
            )
            self.dao.session.add(item)
        else:
            item.quantity += points
        return item

    async def get_activity_points_message(self, count: int = 1):
        user = await self.get_user(self.user_id)
        points = await self.store.activity.check_activity_points(
            self.user_id,
            count * ACTIVITY_POINTS_MESSAGE * settings.activity_points_factor,
            GET_ACTIVITY_POINTS_LIMIT_TTL_MESSAGE, 
            GET_ACTIVITY_POINTS_LIMIT_MESSAGE
        )
        item = await self.get_activity_points(user, points)
        await self.dao.flush()
        self.botlog.get_activity_points(points, item.quantity, 'награда за сообщения')
        return AnswerActivityPoints(
            user=self.return_query_body(user),
            purpose=self.return_query_body(user),
            activity_points=item.quantity,
            get_activity_points=points,
        )

    async def get_activity_points_question(self):
        user = await self.get_user(self.user_id)
        item = await self.get_activity_points(user, ACTIVITY_POINTS_QUESTION)
        await self.dao.flush()
        self.botlog.get_activity_points(ACTIVITY_POINTS_QUESTION, item.quantity, 'награда за правильный ответ на вопрос')
        return item, ACTIVITY_POINTS_QUESTION

    async def reset_activity_points_limit(self, purpose_user_id: int):
        self.check_permission()
        target = await self.get_user(purpose_user_id)
        await self.store.activity.reset_activity_points_limit(purpose_user_id)
        admin = await self.get_user(self.user_id)
        return await self._activity_points_answer(admin, target)


    async def get_activity_points_count(self):
        user = await self.get_user(self.user_id)
        return await self._activity_points_answer(user, user)
