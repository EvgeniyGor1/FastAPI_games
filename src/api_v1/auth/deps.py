import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status

from src.api_v1.auth.active_sessions import active_sessions
from src.api_v1.security import COOKIE_SESSION_ID_KEY, validate_password
from src.database import async_session_maker
from src.api_v1.user.cruds import get_user_by_name
from src.models import User

security = HTTPBasic()


async def get_auth_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> User:

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    async with async_session_maker() as session:
        user = await get_user_by_name(session, credentials.username)

    if not user:
        raise unauthed_exc

    if not validate_password(credentials.password, user.hashed_password):
        raise unauthed_exc

    return user


async def get_session_id(request: Request) -> str:
    session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login to proceed",
            headers={"WWW-Authenticate": "Basic"},
        )

    return session_id


async def get_current_session_user(
    session_id: str = Depends(get_session_id),
) -> (uuid.UUID, User):
    user = active_sessions.get(session_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user


async def validate_admin(
    user: Annotated[User, Depends(get_current_session_user)],
):

    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="unauthorized",
        )
