from collections.abc import AsyncGenerator
from urllib.parse import quote_plus

from app.shared.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

password = quote_plus(settings.POSTGRES_PASSWORD)

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{password}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
