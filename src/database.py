import logging

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from src.config import db_settings


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

async_engine = create_async_engine(db_settings.DATABASE_URI, echo=True)
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def session_dependency() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
