from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload, joinedload
from app.base_dao import BaseDAO
from app.companies.models import Company
from app.database import async_session_maker
from app.dependencies import get_session
from app.vacancies.models import Responses, Tag, Vacancy, TagsVacancies


class VacancyDAO(BaseDAO):
    @classmethod
    async def get_tags_by_ids(cls, tag_ids: list):
        async with async_session_maker() as session:
            result = await session.execute(select(Tag).filter(Tag.id.in_(tag_ids)))
            return result.scalars().fetchall()

    @classmethod
    async def get_vacancies(cls):
        async with async_session_maker() as session:
            vacancies = await session(
                select(Vacancy)
                .order_by(Vacancy.created.desc())
                .options(
                    joinedload(Vacancy.company).load_only(Company.logo, Company.name)
                )
                .options(selectinload(Vacancy.tags))
            )
        return vacancies.scalars().all()

    @classmethod
    async def get_vacancy(cls, v_id):
        async with async_session_maker() as session:
            res_vac = await session.execute(
                select(Vacancy)
                .where(Vacancy.id == v_id)
                .options(selectinload(Vacancy.tags))
            )
            vacancy = res_vac.scalars().first()
            company = await session.execute(
                select(Company)
                .where(Company.id == vacancy.company_id)
                .options(
                    selectinload(Company.vacancies).load_only(
                        Vacancy.title,
                    )
                )
            )
            return {"vacancy": vacancy, "company": company.scalars().first()}

    @classmethod
    async def create_vacancy(cls, new_vacancy):
        async with async_session_maker() as session:
            result = await session.execute(
                insert(Vacancy).values(**new_vacancy).returning(Vacancy.id)
            )
            v_id = result.scalars().first()
            await session.commit()
            return v_id

    @classmethod
    async def add_tags(cls, tags, v_id):
        async with async_session_maker() as session:
            for tag in tags:
                await session.execute(
                    insert(TagsVacancies).values(tag_id=tag.id, vacancy_id=v_id)
                )
            await session.commit()
            return True


class ResponseDAO:
    @classmethod
    async def create_response(
        cls, user_id: int, vacancy_id: int, cover_letter: str | None = None
    ):
        session = get_session()
        response = await session.execute(
            insert(Responses)
            .values(user_id=user_id, vacancy_id=vacancy_id, cover_letter=cover_letter)
            .returning(Responses)
        )
        return response
