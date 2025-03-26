from typing import Annotated
import uuid

from fastapi import APIRouter, status, Depends, HTTPException
from pydantic import EmailStr, PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.deps import admin_permission
from src.api_v1.user import cruds
from src.api_v1.user.cruds import get_user_by_email
from src.database import session_dependency
from src.models.user import UserRegister, UserPublic, User

router = APIRouter(tags=["user"])
user_management = APIRouter(
    tags=["user management"],
    dependencies=[Depends(admin_permission)],
)


@router.post(
    "/sign_up/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
)
async def create_user(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    user_in: UserRegister,
):

    user = await get_user_by_email(session, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await cruds.create_user(session, user_in)
    await session.commit()
    await session.refresh(user)
    return user


@user_management.get(
    "/users_list/",
    response_model=list[User],
)
async def get_users(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    limit: PositiveInt = 10,
):
    users = await cruds.get_users(session, limit)
    await session.commit()
    return users


@user_management.get(
    "/{email}/",
    response_model=UserPublic,
)
async def get_user_by_email(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    email: EmailStr,
):
    user = await cruds.get_user_by_email(session, email)
    return user


@router.get(
    "/id/{id}/",
    response_model=UserPublic,
)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    user_id: uuid.UUID,
):

    user = await cruds.get_user_by_id(session, user_id)
    await session.commit()
    return user


@router.get(
    "/profile/{user_name}/",
    response_model=UserPublic,
)
async def get_user_by_name(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    user_name: str,
):

    user = await cruds.get_user_by_name(session, user_name)
    await session.commit()
    return user


@user_management.delete(
    "/delete/",
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    user_id: uuid.UUID,
):

    await cruds.delete_user_no_authorization(session, user_id)
    await session.commit()

    return "User successfully deleted"
