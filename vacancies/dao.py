from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from app.base_dao import BaseDAO
from app.database import async_session_maker
from app.vacancies.models import Tag, Vacancy, TagsVacancies


class VacancyDAO(BaseDAO):
    @classmethod
    async def get_tags_by_ids(cls, tag_ids: list):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Tag).filter(Tag.id.in_(tag_ids))
            )
            return result.scalars().fetchall()
    
    @classmethod
    async def get_vacancy(cls, v_id):
        async with async_session_maker() as session:
            vacancy = await session.execute(
                select(Vacancy).where(Vacancy.id == v_id).
                options(selectinload(Vacancy.tags))
            )
            return vacancy.scalars().first()
    
    @classmethod
    async def create_vacancy(cls, new_vacancy, tags):
        async with async_session_maker() as session:
            result = await session.execute(
                insert(Vacancy).values(**new_vacancy).returning(Vacancy.id)
            )
            v_id = result.scalars().first()
            await session.commit()
            vacancy = await cls.get_vacancy(v_id)
            for tag in tags:
                vacancy.tags.append(tag)
                await session.execute(insert(TagsVacancies).values(
                    tag_id=tag.id, vacancy_id=vacancy.id
                ))
            await session.commit()
            return vacancy