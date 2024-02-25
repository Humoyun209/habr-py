from sqlalchemy import insert, select, update
from app.database import async_session_maker


class BaseDAO:
    @classmethod
    async def get_list(cls, model):
        async with async_session_maker() as session:
            result = await session.execute(select(model))
            return result.scalars().all()

    @classmethod
    async def create(cls, model, **kwargs):
        async with async_session_maker() as session:
            result = await session.execute(
                insert(model).values(**kwargs).returning(model)
            )
            await session.commit()
            return result.scalars().first()

    @classmethod
    async def edit(cls, model, **kwargs):
        async with async_session_maker() as session:
            result = await session.execute(
                update(model).values(**kwargs).returning(model)
            )
            await session.commit()
            return result.scalars().first()

    @classmethod
    async def get(cls, model, model_id):
        async with async_session_maker() as session:
            result = await session.execute(select(model).where(model.id == model_id))
            return result.scalars().first()
