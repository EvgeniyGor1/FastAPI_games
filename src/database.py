from typing import AsyncGenerator
import logging

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from src.config import settings


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_async_engine(settings.DATABASE_URI, echo=True)
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def session_dependency() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        return session
