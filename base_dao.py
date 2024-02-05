from sqlalchemy import insert, select
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
                insert(model).values(**kwargs).returning(model.id)
            )
            await session.commit()
            return result.scalars().one()