from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


from app.config import Settings

settings = Settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.db.DB_USER}:{settings.db.DB_PASS}@{settings.db.DB_HOST}:{settings.db.DB_PORT}/{settings.db.DB_NAME}"

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
