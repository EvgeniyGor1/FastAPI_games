from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    async_scoped_session,
)

from src.config import settings


engine = create_async_engine(settings.DATABASE_URI)
async_session_maker = async_sessionmaker(engine, xpire_on_commit=False, echo=True)


def get_scoped_session() -> async_scoped_session[AsyncSession]:
    session = async_scoped_session(
        session_factory=async_session_maker,
        scopefunc=current_task,
    )
    return session


async def session_dependency() -> AsyncSession:
    session = get_scoped_session()
    yield session
    await session.remove()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
