import uuid
from typing import Annotated


from fastapi import Depends
import sqlmodel as sm
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import session_dependency
from src.models.game import Game, GameBase, GamePublic
from src.config import constants
from ..utils import create_img_file, delete_img_file


async def create_game(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    game: GameBase,
) -> Game:

    _id = uuid.uuid4()
    cover_path = constants.WORK_DIR + f"\\images\\covers\\{_id}.png"
    game = Game.model_validate(game, update={"id": _id, "cover_path": cover_path})
    await create_img_file(game.cover_path)
    try:
        session.add(game)
        await session.commit()
        await session.refresh(game)
        return game
    except Exception:
        await delete_img_file(game.cover_path)


async def delete_game_by_name(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    game_name: str,
):

    stmt = sm.delete(Game).where(Game.name == game_name)  # noqa ;Type checker bug?
    await session.execute(stmt)
    await session.commit()


async def get_game_by_name(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    game_name: str,
) -> GameBase | None:

    stmt = sm.select(Game).where(Game.name == game_name)  # noqa ;Type checker bug?
    game = await session.scalars(stmt)
    game = game.first()
    await session.commit()
    if game:
        return GameBase.model_validate(game)

    return None


async def get_games(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    _limit: int = 100,
) -> Sequence[Game]:

    stmt = (
        sm.select(GamePublic).limit(_limit).order_by(Game.name)
    )  # noqa ;Type checker bug?
    games = await session.execute(stmt)
    return games.all()
