from pathlib import Path
import os
from enum import Enum

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class CachingType(Enum):
    redis_ = "redis"
    python_dict = "dict"


class Constants(BaseSettings):
    CACHING_TYPE: CachingType = CachingType.redis_
    if os.name == "nt":
        CACHING_TYPE: CachingType = CachingType.python_dict
        WORK_DIR: str = str(Path(__file__).parent.parent) + "\\"
    else:
        WORK_DIR: str = str(Path(__name__).parent.parent) + "/"


constants = Constants()


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=constants.WORK_DIR + ".env",
        extra="allow",
    )

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    POSTGRES_DB: str

    @computed_field
    def DATABASE_URI(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                username=self.DB_USER,
                password=self.DB_PASS,
                host=self.DB_HOST,
                port=self.DB_PORT,
                path=self.POSTGRES_DB,
            )
        )


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=constants.WORK_DIR + ".env",
        extra="allow",
    )

    REDIS_HOST: str
    REDIS_PORT: int
    DECODE_RESPONSE: bool = False


db_settings = DbSettings()  # noqa
redis_settings = RedisSettings()  # noqa
