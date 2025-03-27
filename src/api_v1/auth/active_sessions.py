from datetime import datetime
import uuid
from collections.abc import Callable
from typing import Type, TypeVar

import redis
from pydantic import BaseModel, EmailStr

from src.config import redis_settings, CachingType, constants
from src.models import User


class RedisAdaptor(redis.Redis):
    """Adaptor to work with redis using pydantic model"""

    PydanticModel = TypeVar("PydanticModel", bound=BaseModel)

    def __init__(
        self,
        model: Type[PydanticModel],
        *args,
        **kwargs,
    ):
        """Model = BaseModel pydantic type to work with"""

        super().__init__(*args, **kwargs)
        self.PydanticModel = model
        self.model_fields = list(self.PydanticModel.model_fields.keys())

    def __setitem__(self, session_id: str, model: BaseModel):
        mapped = self.serialize(model)
        self.hset(session_id, mapping=mapped)

    def __getitem__(self, session_id):
        fields = self.hmget(session_id, self.model_fields)
        return self.deserialize(self.model_fields, fields)

    def get(self, session_id):
        fields = self.hmget(session_id, self.model_fields)
        return self.deserialize(self.model_fields, fields)

    def set(self) -> Callable:
        """Redis hset"""
        return self.hset

    def pop(self, session_id: str) -> dict:
        """Dict pop for redis hash table"""
        fields = self.hmget(session_id, self.model_fields)
        user_dict = self.deserialize(self.model_fields, fields)
        self.delete(session_id)
        return user_dict

    def serialize(self, model: BaseModel) -> dict:
        mapped = model.model_dump()
        for key in mapped.keys():
            if type(mapped[key]) != bytes:
                mapped[key] = str(mapped[key])
            else:
                mapped[key] = mapped[key].decode()

        return mapped

    def deserialize(self, class_fields: list, class_values: list) -> dict:
        class_dict = {
            fields: values for fields, values in zip(class_fields, class_values)
        }
        return class_dict


def generate_session_id() -> str:
    return uuid.uuid4().hex


if constants.CACHING_TYPE == CachingType.redis_:
    sessions_cache = RedisAdaptor(
        model=User,
        host=redis_settings.REDIS_HOST,
        port=redis_settings.REDIS_PORT,
        decode_responses=redis_settings.DECODE_RESPONSE,
    )
else:
    sessions_cache = {}


async def create_user_session(user: User) -> str:
    """Generate and return session id"""

    session_id = generate_session_id()
    sessions_cache[session_id] = user
    return session_id


async def delete_user_session(session_id: str) -> None:
    sessions_cache.pop(session_id)


async def get_session_user(session_id: str) -> User:
    user_dict = sessions_cache.get(session_id)
    user_dict["email"] = EmailStr._validate(user_dict["email"])
    user_dict["is_active"] = bool(user_dict["is_active"])
    user_dict["is_superuser"] = bool(user_dict["is_superuser"])
    user_dict["id"] = uuid.UUID(user_dict["id"])
    user_dict["hashed_password"] = bytes(user_dict["hashed_password"].encode())
    user_dict["registered_at"] = datetime.fromisoformat(user_dict["registered_at"])

    return User(**user_dict)
