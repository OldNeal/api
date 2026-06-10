from typing import Generic, TypeVar
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from app.db.base import Base
from datetime import datetime, date

T = TypeVar("T", bound=Base)

class BaseDAO(Generic[T]):
    model: type[T] = Base# Устанавливается в дочернем классе

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session
    
    async def find_one_or_none_by_id(self, data_id: int):
        # Найти запись по ID
        try:
            query = select(self.model).filter_by(id=data_id)
            result = await self.session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise

    async def find_one_or_none(self, filters: dict):
        # Найти одну запись по фильтрам
        try:
            query = select(self.model).filter_by(**filters)
            result = await self.session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise

    async def select_for_ids(self, ids: list[int],                        
                            ):
        try:
            query = select(self.model).where(self.model.id.in_(ids))
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise        

    async def find_for_date(self, date: date                         
                            ):
        try:
            query = select(self.model).filter(func.date(self.model.created_at) == date)
            result = await self.session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise       

    async def find_all(self, filters: dict | None = None, order_by: dict | None = None):
        filter_dict = filters if filters else {}
        order_dict = order_by if order_by else {}        

        try:
            query = select(self.model).filter_by(**filter_dict).order_by(**order_dict)
            result = await self.session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise

    async def add(self, values: dict):
        # Добавить одну запись
        try:
            new_instance = self.model(**values)
            self.session.add(new_instance)
            await self.session.flush()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
        return await self.find_one_or_none_by_id(new_instance.id)

    async def add_dict(self, values: dict):
        # Добавить одну запись
        try:
            new_instance = self.model(**values)
            self.session.add(new_instance)
            await self.session.flush()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
        return new_instance
    
    async def add_many(self, instances: list[dict]):
        # Добавить несколько записей
        new_instances = [self.model(**values) for values in instances]
        self.session.add_all(new_instances)
        try:
            await self.session.flush()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
        return new_instances
        
    async def add_or_update(self, data: dict, **filters):
        try:
            select_data: Base = await self.find_one_or_none(filters=filters)
            
            if select_data:
                update = await self.update_one_by_id_no_valid(select_data.id, values_dict=data)
                datas = await self.find_one_or_none(filters=filters)
            else:
                datas = self.model(**data)
                self.session.add(datas)
            await self.session.flush()
            return datas
        except Exception as e:
            await self.session.rollback()
            raise

    async def update_one_by_id_no_valid(self, data_id: int, values_dict: dict):
        try:
            record = await self.session.get(self.model, data_id)
            for key, value in values_dict.items():
                setattr(record, key, value)
            await self.session.flush()
            return True
        except SQLAlchemyError as sqle:
            raise   
        except Exception as e:
            raise   

    async def update_one_by_id(self, data_id: int, values: dict):
        try:
            record = await self.session.get(self.model, data_id)
            return await self.update_one(record=record, values=values)
        except SQLAlchemyError as e:
            raise   
  
    async def update_one(self, record: Base, values: dict):
        try:
            for key, value in values.items():
                setattr(record, key, value)
            await self.session.flush()
            return record
        except SQLAlchemyError as e:
            raise          

    async def update_many(self, filters: dict, values: dict):
        try:
            stmt = (
                update(self.model)
                .filter_by(**filters)
                .values(**values)
            )
            result = await self.session.execute(stmt)
            await self.session.flush()
            return result.rowcount
        except SQLAlchemyError as e:
            raise e

    async def update_many_for_ids(self, ids: list[int], values: dict):
        try:
            stmt = update(self.model).where(self.model.id.in_(ids)).values(**values)
            result = await self.session.execute(stmt)
            await self.session.flush()
            return result.rowcount
        except SQLAlchemyError as e:
            raise e        
        
    async def delete_one_by_id(self, data_id: int):
        # Найти запись по ID
        try:
            data = await self.session.get(self.model, data_id)
            if data:
                await self.session.delete(data)
                await self.session.flush()
            return True
        except SQLAlchemyError as e:
            raise

    async def delete_many(self, filters: dict | None = None):
        if filters:
            stmt = delete(self.model).filter_by(**filters)
        else:
            stmt = delete(self.model)
        try:
            result = await self.session.execute(stmt)
            await self.session.flush()
            return result.rowcount
        except SQLAlchemyError as e:
            raise

    async def delete_many_for_ids(self, ids: list[int]):
        stmt = delete(self.model).where(self.model.id.in_(ids))
        try:
            result = await self.session.execute(stmt)
            await self.session.flush()
            return result.rowcount
        except SQLAlchemyError as e:
            raise

    async def flush(self):
        await self.session.flush()  

    async def commit(self):
        await self.session.commit()    

    async def close(self):
        await self.session.close()        
        
    async def rollback(self):
        await self.session.rollback()  