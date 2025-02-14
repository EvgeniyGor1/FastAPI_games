from typing import Annotated
import uuid

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user import cruds
from src.api_v1.user.cruds import get_user_by_email
from src.database import session_dependency
from src.models import UserRegister, UserPublic

router = APIRouter(tags=["user"])


@router.post(
    "/",
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
    return user


@router.get("/", response_model=UserPublic)
async def get_users(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    limit: int = 10,
):

    return await cruds.get_users(session, limit)


@router.get("/{user_id}", response_model=UserPublic)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    user_id: uuid.UUID,
):

    return await cruds.get_user_by_id(session, user_id)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_no_authorization(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    user_id: uuid.UUID,
):

    await cruds.delete_user_no_authorization(session, user_id)

    return "User successfully deleted"
