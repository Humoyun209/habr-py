from app.base_dao import BaseDAO
from app.companies.models import Company
from app.users.models import User
from app.vacancies.models import City
from app.database import async_session_maker
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import selectinload, joinedload


class CityDAO(BaseDAO):
    pass


class CompanyDAO(BaseDAO):
    @classmethod
    async def get_company_with_all_data(cls, company_id: int) -> Company:
        async with async_session_maker() as session:
            query = (
                select(Company)
                .where(Company.id == company_id)
                .options(joinedload(Company.owner).defer(User.password))
                .options(joinedload(Company.city))
                .options(selectinload(Company.followers).defer(User.password))
                .options(selectinload(Company.vacancies))
            )
            result = await session.execute(query)
            return result.scalars().first()
    
    @classmethod
    async def company_ids(cls, user_id):
        async with async_session_maker() as session:
            query = select(Company.id).where(Company.user_id == user_id)
            result = await session.execute(query)
            return result.fetchall()
