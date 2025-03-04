from fastapi import APIRouter


from src.api_v1.user.views import router as user_router, user_management
from src.api_v1.game.views import router as game_router, game_management
from src.api_v1.auth.cookie_login import cookie_router


routers = APIRouter()
routers.include_router(router=user_router, prefix="/users")
routers.include_router(router=user_management, prefix="/users/management")
routers.include_router(router=game_router, prefix="/users/games")
routers.include_router(router=game_management, prefix="/users/games/management")
routers.include_router(router=cookie_router, prefix="/cookie")
