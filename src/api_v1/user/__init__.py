from fastapi import APIRouter

from src.api_v1.user.views import router as user_router


router = APIRouter()
router.include_router(
    router=user_router,
    prefix="/users",
)
