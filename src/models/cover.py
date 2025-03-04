import uuid

from sqlmodel import SQLModel, Field, AutoString, Relationship

from src.models.game import Game


class Cover(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    path: str = Field(nullable=False, sa_type=AutoString)
    game_id: uuid.UUID = Field(
        foreign_key="game.id",
        nullable=False,
        ondelete="CASCADE",
        index=True,
    )

    game: Game = Relationship(back_populates="cover")
