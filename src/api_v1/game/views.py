from typing import Annotated


from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.game import cruds
from src.database import session_dependency
from src.models.game import Game, GameCreate, GameBase

router = APIRouter(tags=["game"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=GameCreate,
)
async def load_game_in_db(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    game: GameBase,
):

    game_db = await cruds.get_game_by_name(session, game.name)
    if game_db:
        raise HTTPException(
            status_code=400,
            detail="The game name already exists in the database.",
        )
    game = await cruds.create_game(session, game)
    return game


@router.get(
    "/",
    response_model=Game,
)
async def get_game_by_name(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    game: Game,
):
    pass
