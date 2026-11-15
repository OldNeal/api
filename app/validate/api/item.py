from pydantic import Field
from app.validate.api.base import (
    AnswerBaseBody,
    AnswerBody,
    BaseAPIValidate,
    Page,
    QueryBody,
)


class QueryItemChange(QueryBody):
    purpose_user_id: int
    item_id: int
    quantity: int = Field(default=1, gt=0)


class ItemInfo(BaseAPIValidate):
    item_id: int
    name: str
    tag: str
    hash: str
    description: str | None = None
    emodzi: str | None = None
    custom_emodzi_id: str | None = None
    data: dict
    quantity: int | None = None


class AnswerItems(AnswerBaseBody):
    items: list[ItemInfo]
    page: Page | None = None
    count: int = 0


class AnswerInventory(AnswerBody):
    items: list[ItemInfo]
    page: Page | None = None
    count: int = 0


class AnswerItemChange(AnswerBody):
    item: ItemInfo
