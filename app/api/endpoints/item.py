from fastapi import APIRouter, Depends, Path, Query
from app.api.depends.session import get_session
from app.exception import get_exception_codes
from app.service.item import ItemService
from app.validate.api.base import QueryBody
from app.validate.api.item import (
    AnswerInventory,
    AnswerItemChange,
    AnswerItems,
    ItemInfo,
    QueryItemChange,
)


item_router = APIRouter(
    prefix='/item',
    tags=['item'],
    responses=get_exception_codes(types=['item']),
)


@item_router.post('/give', response_model=AnswerItemChange)
async def item_give(
    query: QueryItemChange,
    session=Depends(get_session()),
):
    return await ItemService(
        session,
        query.user_id,
        purpose_user_id=query.purpose_user_id,
        is_admin=query.is_admin,
    ).give(query.item_id, query.quantity)


@item_router.post('/take', response_model=AnswerItemChange)
async def item_take(
    query: QueryItemChange,
    session=Depends(get_session()),
):
    return await ItemService(
        session,
        query.user_id,
        purpose_user_id=query.purpose_user_id,
        is_admin=query.is_admin,
    ).take(query.item_id, query.quantity)


@item_router.post('/inventory', response_model=AnswerInventory)
async def item_inventory(
    query: QueryBody,
    user_id: int | None = Query(None, description='ID пользователя'),
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
    session=Depends(get_session()),
):
    return await ItemService(
        session,
        query.user_id,
        purpose_user_id=user_id,
        is_admin=query.is_admin,
    ).inventory(page, per_page)


@item_router.get('/list', response_model=AnswerItems)
async def item_list(
    page: int | None = Query(None, ge=0, description='Номер страницы'),
    per_page: int = Query(5, ge=1, description='Результатов на странице'),
    session=Depends(get_session()),
):
    return await ItemService(session).list_items(page, per_page)


@item_router.get('/{item_id}', response_model=ItemInfo)
async def item_info(
    item_id: int = Path(gt=0, description='ID предмета'),
    session=Depends(get_session()),
):
    return await ItemService(session).get_item(item_id)

@item_router.post('/inventory/item', response_model=ItemInfo)
async def item_inventory_info(
    query: QueryBody,
    item_id: int = Query(gt=0, description='ID предмета', alias='id'),
    session=Depends(get_session()),
):
    return await ItemService(session, query.user_id).get_inventory_item(item_id)
