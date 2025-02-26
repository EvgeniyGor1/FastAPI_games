import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.models.cover import Cover


class GameBase(SQLModel):
    name: str = Field(max_length=255, unique=True, index=True)
    description: str
    price: Decimal


class Game(GameBase, table=True):
    id: uuid.UUID = Field(primary_key=True)
    cover_path: str

    cover: "Cover" = Relationship(back_populates="game", cascade_delete=True)


class GameCreate(GameBase):
    id: uuid.UUID


class GamePublic(GameBase):
    pass
