from typing import Optional

from sqlalchemy import select, insert

from fastapi_learning.app.database import async_session_maker, Base


class BaseDAO:
    model: Optional['Base'] = None

    # @classmethod
    # async def find_by_id(cls, model_id: int):
    #     print(model_id)
    #     print(type(model_id))
    #     async with async_session_maker() as session:
    #         stmt = select(cls.model.__table__.columns).filter_by(id=model_id)
    #         print(stmt)
    #         query = await session.execute(stmt)
    #         print(query)
    #         result = query.mappings().one_or_none()
    #         print(result)
    #         return result

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**filter_by)
            query = await session.execute(stmt)
            result = query.mappings().one_or_none()
            return result

    @classmethod
    async def find_all(cls, **kwargs):
        async with async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**kwargs)
            query = await session.execute(stmt)
            result = query.mappings().all()
            return result

    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model.__table__.columns.id)
            result = await session.execute(stmt)
            result = result.mappings().first()
            await session.commit()
            return result
