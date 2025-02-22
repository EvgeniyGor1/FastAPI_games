import uuid
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.models.cover import Cover


class GameBase(SQLModel):
    name: str


class Game(GameBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)

    cover: "Cover" = Relationship(back_populates="game", cascade_delete=True)
