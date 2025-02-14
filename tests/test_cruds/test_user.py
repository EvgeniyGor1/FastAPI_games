import asyncio

import pytest
import pytest_asyncio
from sqlmodel import select

from src.api_v1.user.cruds import get_user_by_email, create_user, get_user_by_id
from src.database import async_session_maker
from src.models import User, UserRegister


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(loop_scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
        await session.close()


@pytest.mark.asyncio
@pytest.mark.once
async def test_create_user():
    user_test = UserRegister(
        username="test_user", email="test@example.com", password="testtest"
    )

    user = await create_user(session, user_test)

    assert user is not None
    assert user.email == "test@example.com"
    assert user.username == "test_user"

    stmt = select(User).where(User.email == user.email)  # noqa ;Type checker bug?
    result = await session.execute(stmt)
    user_from_db = result.scalars().first()

    assert user_from_db is not None
    assert user_from_db.email == "test@example.com"


@pytest.mark.asyncio
@pytest.mark.regular
async def test_get_user_by_email(session):
    email = "test@example.com"

    user = await get_user_by_email(session, email)

    assert user is not None
    assert user.email == "test@example.com"
    assert user.username == "test_user"


@pytest.mark.asyncio
@pytest.mark.regular
async def test_get_user_by_id(session):
    email = "test@example.com"

    user = await get_user_by_email(session, email)

    user_by_id = await get_user_by_id(session, user.id)

    assert user_by_id is not None
    assert user_by_id.email == "test@example.com"
    assert user_by_id.username == "test_user"
