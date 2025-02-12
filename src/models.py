import datetime
import uuid
from typing import Annotated

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, AutoString, Relationship


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(min_length=8, max_length=40)
    registered_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )


class UserRegister(SQLModel):
    username: str
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


class GameBase(SQLModel):
    name: str


class Game(GameBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    cover_id: uuid.UUID = Field(foreign_key="cover.id")

    cover: "Cover" = Relationship(back_populates="game")


class Cover(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        ondelete="CASCADE",
    )
    path: str = Field(nullable=False, sa_type=AutoString)
    game_id: uuid.UUID = Field(
        foreign_key="game.id",
        nullable=False,
        ondelete="CASCADE",
    )

    game: Game = Relationship(back_populates="cover")
