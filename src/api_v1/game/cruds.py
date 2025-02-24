import uuid
from typing import Annotated


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import session_dependency
from src.models.game import GameCreate, Game, GameBase
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


async def get_game_by_name(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    name: str,
):

    pass
