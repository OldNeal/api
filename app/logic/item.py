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
            inventory = InventoryDB()
            purpose.inventory = inventory
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
