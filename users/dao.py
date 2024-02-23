import asyncio
from app.base_dao import BaseDAO
from app.database import async_session_maker
from sqlalchemy import insert, or_, select
from sqlalchemy.orm import selectinload, joinedload, deferred, defer, load_only
from sqlalchemy.exc import IntegrityError
from app.users.models import Resume, User
from app.users.schemas import UserLogin
from app.vacancies.models import Vacancy
from app.companies.models import Company
from sqlalchemy import case, func


class UserDAO:
    @classmethod
    async def get_users(cls):
        async with async_session_maker() as session:
            users = await session.execute(select(User.id, User.username, User.email))
            return users.fetchall()

    @classmethod
    async def get_username_and_pass(cls, username: str):
        async with async_session_maker() as session:
            user = await session.execute(
                select(User)
                .options(load_only(User.username, User.password))
                .where(User.username == username)
            )
            return user.scalars().first()

    @classmethod
    async def get_user(cls, username):
        async with async_session_maker() as session:
            user = await session.execute(
                select(User)
                .options(defer(User.password))
                .where(User.username == username)
                .options(selectinload(User.companies))
            )
            return user.scalars().first()

    @classmethod
    async def check_unique_user(cls, username, email):
        async with async_session_maker() as session:
            user = await session.execute(
                select(User).where(or_(User.username == username, User.email == email))
            )
            return user.scalars().first()

    @classmethod
    async def create_user(cls, **kwargs):
        async with async_session_maker() as session:
            if not await cls.check_unique_user(
                email=kwargs.get("email"), username=kwargs.get("username")
            ):
                await session.execute(insert(User).values(**kwargs))
                await session.commit()
                return True
            return False

    @classmethod
    async def get_full_data_user(cls, user_id):
        async with async_session_maker() as session:
            user = await session.execute(
                select(User)
                .options(defer(User.password))
                .where(User.id == user_id)
                .options(joinedload(User.resume))
                .options(selectinload(User.companies))
            )
            return user.scalars().first()

    @classmethod
    async def test_case(cls):
        async with async_session_maker() as session:
            query = select(
                User,
                case(
                    (User.username == "humoyun209", "admin"),
                    (User.username == "django", "user"),
                    else_="None",
                ),
            )
            result = await session.execute(query)
            res = result.fetchone()
            return {"user": res[0], "role": res[1]}


class ResumeDAO(BaseDAO):
    @classmethod
    async def create_resume(cls, **kwargs):
        async with async_session_maker() as session:
            resume = await session.execute(
                insert(Resume).values(**kwargs).returning(Resume)
            )
            await session.commit()
            return resume.scalars().first()
