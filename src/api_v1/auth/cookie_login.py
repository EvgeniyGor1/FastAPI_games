from fastapi import APIRouter, Depends, Response, Request

from src.api_v1.auth.active_sessions import create_user_session, delete_user_session
from src.api_v1.auth.deps import get_auth_user, get_current_session_user
from src.api_v1.security import COOKIE_SESSION_ID_KEY
from src.models import User

cookie_router = APIRouter(tags=["cookie"])


@cookie_router.post("/login-cookie/")
async def login(
    response: Response,
    auth_user: User = Depends(get_auth_user),
):

    session_id = await create_user_session(auth_user)
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "Logged"}


@cookie_router.get("/me/")
async def get_current_user(user: User = Depends(get_current_session_user)):
    return f"Hello {user.username}"


@cookie_router.post("/logout/")
async def logout(
    response: Response,
    request: Request,
):

    await delete_user_session(request.cookies.get(COOKIE_SESSION_ID_KEY))
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    return {"result": "Logged out"}
