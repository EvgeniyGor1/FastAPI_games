import uuid

from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
import sqlmodel as sm

from src.models.user import UserRegister, User
from src.security import get_password_hash


async def create_user(
    session: AsyncSession,
    user_register: UserRegister,
) -> User:
    user = User.model_validate(
        user_register,
        update={"hashed_password": get_password_hash(user_register.password)},
    )
    session.add(user)

    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(
    session: AsyncSession,
    user_id: uuid.UUID,
) -> User | None:

    user = await session.get(User, user_id)

    await session.commit()
    return user


async def get_users(
    session: AsyncSession,
    users_limit: int = 10,
) -> Sequence[User]:

    stmt = sm.select(User).limit(users_limit)
    users = await session.scalars(stmt)

    await session.commit()
    return users.all()


async def get_user_by_email(
    session: AsyncSession,
    email: str,
) -> User | None:
    stmt = sm.select(User).where(User.email == email)  # noqa ;Type checker bug?

    session_user = await session.execute(stmt)
    session_user = session_user.scalars().first()
    await session.commit()
    return session_user


async def get_user_by_name(
    session: AsyncSession,
    user_name: str,
) -> User | None:

    stmt = sm.select(User).where(User.username == user_name)  # noqa ;Type checker bug?

    user = await session.scalars(stmt)
    await session.commit()
    return user.one_or_none()


async def delete_user_no_authorization(
    session: AsyncSession,
    user_id: uuid.UUID,
) -> None:

    stmt = sm.delete(User).where(User.id == user_id)  # noqa ;Type checker bug?
    await session.execute(stmt)
    await session.commit()
