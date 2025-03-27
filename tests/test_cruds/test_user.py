import asyncio

import pytest
import pytest_asyncio
from sqlmodel import select

from src.api_v1.user.cruds import get_user_by_email, create_user, get_user_by_id
from src.database import async_session_maker
from src.models.user import User, UserRegister


@pytest_asyncio.fixture
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def session():
    async with async_session_maker() as session:
        yield session
        await session.close()


@pytest.mark.asyncio(scope="function")
@pytest.mark.once
async def test_create_user(session):
    test_name = "pytest_user"
    test_email = "pytest@example.com"
    test_password = "pytestpytest"
    user_test = UserRegister(
        username=test_name,
        email=test_email,
        password=test_password,
    )

    user = await create_user(session, user_test)

    await session.refresh(user)

    assert user is not None
    assert user.email == test_email
    assert user.username == test_name

    stmt = select(User).where(User.email == user.email)  # noqa ;Type checker bug?
    result = await session.execute(stmt)
    user_from_db = result.scalars().first()
    await session.commit()

    assert user_from_db is not None
    assert user_from_db.email == test_email


@pytest.mark.asyncio(scope="function")
@pytest.mark.regular
async def test_get_user_by_email(session):
    test_email = "pytest@example.com"

    user = await get_user_by_email(session, test_email)

    await session.commit()

    assert user is not None
    assert user.email == test_email
    assert user.username == "pytest_user"


@pytest.mark.asyncio(scope="function")
@pytest.mark.regular
async def test_get_user_by_id(session):
    test_email = "pytest@example.com"

    user = await get_user_by_email(session, test_email)

    user_by_id = await get_user_by_id(session, user.id)

    session.aclose()
    await session.commit()

    assert user_by_id is not None
    assert user_by_id.email == test_email
    assert user_by_id.username == "pytest_user"
