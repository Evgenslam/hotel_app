from sqlalchemy import delete, insert, select, update
from app.database import async_session_maker


class BaseDAO:
    model=None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()
        

    classmethod
    async def update(cls, filters: dict, **data):
        async with async_session_maker() as session:
            stmt = (
            update(cls.model).
            filter_by(**filters).
            values(**data)
        )
            await session.execute(stmt)
            await session.commit()      
    
    
    @classmethod
    async def delete(cls, **filters):
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(**filters)
            result = result = await session.execute(stmt)
            await session.commit()
            return result.rowcount 