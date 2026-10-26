from functools import wraps
from typing import Optional
from sqlalchemy import text
from app.db.base import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dao.models import DAO

def connection(isolation_level: Optional[str] = None, commit: bool = True):
    """
    Декоратор для управления сессией с возможностью настройки уровня изоляции и коммита.
    Параметры:
    - `isolation_level`: уровень изоляции для транзакции (например, "SERIALIZABLE").
    - `commit`: если `True`, выполняется коммит после вызова метода.
    """
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    if isolation_level:
                        await session.execute(text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"))
                    result = await method(*args, session=session, **kwargs)
                    if commit:
                        await session.commit()
                    return result
                except Exception as e:
                    await session.rollback()
                    raise 
                finally:
                    await session.close()
        return wrapper
    return decorator

def get_dao(commit: bool = True):
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    dao = DAO(session)
                    result = await method(*args, dao=dao, **kwargs)
                    if commit:
                        await dao.commit()
                    return result
                except Exception as e:
                    await dao.rollback()
                    raise 
                finally:
                    await dao.close()
        return wrapper
    return decorator