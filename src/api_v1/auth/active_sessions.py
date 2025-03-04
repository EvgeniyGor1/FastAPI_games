from src.api_v1.utils import generate_session_id
from src.models import User

active_sessions: dict[str, User] = {}


async def create_user_session(user: User) -> str:
    """Return session id"""

    session_id = await generate_session_id()
    active_sessions[session_id] = user
    return session_id


async def delete_user_session(session_id: str) -> None:

    active_sessions.pop(session_id)
