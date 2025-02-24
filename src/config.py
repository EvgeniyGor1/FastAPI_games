from pathlib import Path

from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env")
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


class Constants(BaseSettings):
    WORK_DIR: str = str(Path(__file__).parent.parent)


settings = Config()
constants = Constants()
