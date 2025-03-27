from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Response, Request
from fastapi.params import Depends

from src.api_v1.auth.active_sessions import create_user_session, delete_user_session
from src.api_v1.auth.deps import AuthUserDep, CurrentUserDep, get_current_session_user
from src.api_v1.security import COOKIE_SESSION_ID_KEY, COOKIE_MAX_AGE
from src.models import User
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

cookie_router = APIRouter(tags=["cookie"])


@cookie_router.post("/login-cookie/")
async def login(
    response: Response,
    auth_user: AuthUserDep,
):

    session_id = await create_user_session(auth_user)
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=COOKIE_MAX_AGE)
    response.set_cookie(
        COOKIE_SESSION_ID_KEY,
        session_id,
        expires=expire_at,
    )
    return {"result": f"Logged, {auth_user.username}"}


@cookie_router.get("/me/")
async def get_current_user(user: User = Depends(get_current_session_user)):

    return f"Hello {user.username}"


@cookie_router.post("/me/logout/")
async def logout(
    response: Response,
    request: Request,
):

    await delete_user_session(request.cookies.get(COOKIE_SESSION_ID_KEY))
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    return {"result": "Logged out"}
