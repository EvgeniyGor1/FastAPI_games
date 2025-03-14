from pathlib import Path
import os

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Constants(BaseSettings):
    if os.name == "nt":
        WORK_DIR: str = str(Path(__file__).parent.parent) + "\\"
    else:
        WORK_DIR: str = str(Path(__name__).parent.parent) + "/"


constants = Constants()


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=constants.WORK_DIR + ".env")
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


settings = Config()  # noqa
