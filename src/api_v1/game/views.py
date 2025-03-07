from typing import Annotated


from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.deps import validate_admin
from src.api_v1.game import cruds
from src.database import session_dependency
from src.models.game import Game, GameBase

router = APIRouter(tags=["game"])
game_management = APIRouter(
    tags=["game management"],
    dependencies=[Depends(validate_admin)],
)


@game_management.post(
    "/load_game/",
    status_code=status.HTTP_201_CREATED,
    response_model=Game,
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


@game_management.delete(
    "/delete_game/",
    status_code=status.HTTP_200_OK,
)
async def delete_game_by_name(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    game_name: str,
):

    await cruds.delete_game_by_name(session, game_name)
    return "Game deleted"


@router.get(
    "/{game_name}/",
    response_model=GameBase,
)
async def get_game_by_name(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    game_name: str,
):

    game = await cruds.get_game_by_name(session, game_name)
    if not game:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The game is not found",
        )

    return game


@router.get(
    "/list/",
    response_model=list[GameBase],
)
async def get_games(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    limit: int,
):

    return await cruds.get_games(session, limit)
