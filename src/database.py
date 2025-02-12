from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from src.config import settings


engine = create_async_engine(settings.DATABASE_URI)
async_session_maker = async_sessionmaker(
    engine,
    xpire_on_commit=False,
    echo=True,
)


async def session_dependency() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
