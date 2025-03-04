import bcrypt

COOKIE_SESSION_ID_KEY = "web-app-session-id"


def get_password_hash(password: str | bytes) -> bytes:
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def validate_password(
    password: str | bytes,
    hashed_password: bytes,
) -> bool:

    password = password.encode()
    return bcrypt.checkpw(password, hashed_password)
