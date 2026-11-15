from app.db.models.item import InventoryDB, ItemDB, ItemSketchDB
from app.exception.base import UserDontFind
from app.exception.item import ItemDontFindException, ItemQuantityException
from app.logic.base import BaseLogic
from config import settings
from app.validate.api.base import AnswerActivityPoints
from app.validate.api.item import (
    AnswerInventory,
    AnswerItemChange,
    AnswerItems,
    ItemInfo,
)

ACTIVITY_POINTS_TAG = 'activity_point'
ACTIVITY_POINTS_MESSAGE = 10
GET_ACTIVITY_POINTS_TTL = 60*60*60*24
GET_ACTIVITY_POINTS_LIMIT = 1200

class ItemLogic(BaseLogic):
    def _item_info(self, sketch: ItemSketchDB, quantity: int | None = None):
        return ItemInfo(
            item_id=sketch.id,
            name=sketch.name,
            tag=sketch.tag,
            hash=sketch.hash,
            description=sketch.description,
            emodzi=sketch.emodzi,
            custom_emodzi_id=sketch.custom_emodzi_id,
            data=sketch.data,
            quantity=quantity,
        )

    async def list_items(self, page: int | None = None, per_page: int = 5):
        sketches, count = await self.dao.item_sketch.find_all_paginated(
            page=page,
            per_page=per_page,
        )
        return AnswerItems(
            items=[self._item_info(sketch) for sketch in sketches],
            page=self.pagination(page, per_page, count),
            count=count,
        )

    async def get_item(self, item_id: int):
        sketch = await self.dao.item_sketch.query_by_id(item_id)
        if sketch is None:
            raise ItemDontFindException()
        return self._item_info(sketch)

    async def get_inventory_item(self, item_id: int):
        sketch = await self.dao.item_sketch.query_by_id(item_id)
        if sketch is None:
            raise ItemDontFindException()

        user = await self.get_user(self.user_id, only_user=True)
        inventory = user.inventory
        item = (
            await self.dao.item.query_by_inventory_and_sketch(inventory.id, sketch.id)
            if inventory is not None
            else None
        )
        return self._item_info(sketch, item.quantity if item is not None else 0)

    async def inventory(self, page: int | None = None, per_page: int = 5):
        user = await self.get_user(self.user_id, only_user=True)
        purpose = await self.get_user(self.purpose_user_id)
        inventory = purpose.inventory
        if inventory is None:
            items, count = [], 0
        else:
            items, count = await self.dao.item.query_inventory_paginated(
                inventory.id,
                page,
                per_page,
            )
        return AnswerInventory(
            user=self.return_query_body(user),
            purpose=self.return_query_body(purpose),
            items=[self._item_info(item.sketch, item.quantity) for item in items],
            page=self.pagination(page, per_page, count),
            count=count,
        )

    async def _change_item(self, item_id: int, quantity: int, give: bool):
        self.check_permission()
        user = await self.get_user(self.user_id, only_user=True)
        purpose = await self.dao.user.query_by_user_id(self.purpose_user_id)
        if purpose is None:
            raise UserDontFind()
        sketch = await self.dao.item_sketch.query_by_id(item_id)
        if sketch is None:
            raise ItemDontFindException()

        inventory = purpose.inventory
        if inventory is None:
            if not give:
                raise ItemQuantityException(quantity=quantity, available=0)
            inventory = InventoryDB(user_id=purpose.id)
            purpose.inventory = inventory
            self.dao.session.add(inventory)
            await self.dao.flush()

        item = await self.dao.item.query_by_inventory_and_sketch(
            inventory.id,
            sketch.id,
        )
        
        if give:
            if item is None:
                item = ItemDB(
                    sketch_id=sketch.id,
                    inventory_id=inventory.id,
                    quantity=quantity,
                )
                self.dao.session.add(item)
                new_quantity = quantity
            else:
                item.quantity += quantity
                new_quantity = item.quantity
        else:
            available = item.quantity if item is not None else 0
            if available < quantity:
                raise ItemQuantityException(
                    quantity=quantity,
                    available=available,
                )
            new_quantity = available - quantity
            if new_quantity:
                item.quantity = new_quantity
            else:
                await self.dao.session.delete(item)

        await self.dao.flush()
        return AnswerItemChange(
            user=self.return_query_body(user),
            purpose=self.return_query_body(purpose),
            item=self._item_info(sketch, new_quantity),
        )

    async def give(self, item_id: int, quantity: int):
        return await self._change_item(item_id, quantity, give=True)

    async def take(self, item_id: int, quantity: int):
        return await self._change_item(item_id, quantity, give=False)

    async def _activity_point_sketch(self):
        sketch = await self.dao.item_sketch.query_by_tag(ACTIVITY_POINTS_TAG)
        if sketch is None:
            raise ItemDontFindException()
        return sketch

    async def _activity_point_item(self, user, create: bool = False):
        sketch = await self._activity_point_sketch()
        inventory = user.inventory
        if inventory is None and create:
            inventory = InventoryDB(user_id=user.id)
            user.inventory = inventory
            self.dao.session.add(inventory)
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

    async def get_activity_points(self, message_count: int = 1):
        user = await self.get_user(self.user_id)
        points = await self.store.activity.check_activity_points(
            self.user_id,
            message_count * ACTIVITY_POINTS_MESSAGE * settings.activity_points_factor,
            GET_ACTIVITY_POINTS_TTL, 
            GET_ACTIVITY_POINTS_LIMIT
        )
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
        await self.dao.flush()
        self.botlog.get_activity_points(points, item.quantity)
        return AnswerActivityPoints(
            user=self.return_query_body(user),
            purpose=self.return_query_body(user),
            activity_points=item.quantity,
            get_activity_points=points,
        )



    async def reset_activity_points_limit(self, purpose_user_id: int):
        self.check_permission()
        target = await self.get_user(purpose_user_id)
        await self.store.activity.reset_activity_points_limit(purpose_user_id)
        admin = await self.get_user(self.user_id)
        return await self._activity_points_answer(admin, target)
