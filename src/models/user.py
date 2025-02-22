from datetime import datetime, timezone as tz
import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, DateTime, Column


class UserBase(SQLModel):
    username: str
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    registered_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(tz.utc).replace(microsecond=0),
    )


class UserRegister(SQLModel):
    username: str
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


class UserPublic(SQLModel):
    username: str
    email: EmailStr = Field(unique=True, index=True, max_length=255)
