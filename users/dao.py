import asyncio
from app.database import async_session_maker
from sqlalchemy import insert, or_, select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import IntegrityError
from app.users.models import User
from app.vacancies.models import Vacancy
from app.companies.models import Company

class UserDAO:
    @classmethod
    async def get_users(cls):
        async with async_session_maker() as session:
            users = await session.execute(select(User.id, User.username, User.email))
            return users.fetchall()
    
    @classmethod
    async def get_user(cls, username):
        async with async_session_maker() as session:
            user = await session.execute(
                select(User).where(User.username == username)
                .options(selectinload(User.companies))
            )
            return user.scalars().first()
    
    @classmethod
    async def check_unique_user(cls, username, email):
        async with async_session_maker() as session:
            user = await session.execute(
                select(User).where(or_(
                    User.username == username,
                    User.email == email
                ))
            )
            return user.scalars().first()
            
    @classmethod
    async def create_user(cls, **kwargs):
        async with async_session_maker() as session:
            if not await cls.check_unique_user(
                email=kwargs.get('email'),
                username=kwargs.get('username')
            ):
                await session.execute(
                    insert(User).values(**kwargs)
                )
                await session.commit()
                return True
            return False
            