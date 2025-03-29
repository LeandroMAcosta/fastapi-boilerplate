import os
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config

# Load .env file based on the environment
current_file_dir = Path(__file__).resolve().parent
env_file = f".env.{os.getenv('ENVIRONMENT', 'local')}"
env_path = current_file_dir.parent.parent / env_file
load_dotenv(env_path)
config = Config(str(env_path))


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    APP_NAME: str = config("APP_NAME", default="FastAPI app")
    APP_DESCRIPTION: str = config("APP_DESCRIPTION", default="FastAPI app")


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="postgres")
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="localhost")
    POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int, default=5432)
    POSTGRES_DB: str = config("POSTGRES_DB", default="postgres")
    POSTGRES_ASYNC_PREFIX: str = config("POSTGRES_ASYNC_PREFIX", default="postgresql+asyncpg://")

    @property
    def POSTGRES_URI(self) -> str:
        return f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    POSTGRES_URL: str | None = config("POSTGRES_URL", default=None)


class EnvironmentOption(str, Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    ENVIRONMENT: EnvironmentOption = config(
        "ENVIRONMENT", default=EnvironmentOption.LOCAL, cast=lambda x: EnvironmentOption(x)
    )


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    JWT_SECRET: str = config("JWT_SECRET")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", default="HS256")
    JWT_EXPIRATION_TIME: int = config("JWT_EXPIRATION", cast=int, default=15)

    # Add these new settings
    GOOGLE_CLIENT_ID: str = config("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = config("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = config("GOOGLE_REDIRECT_URI")


class Settings(AppSettings, PostgresSettings, EnvironmentSettings, LoggingSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    DEBUG: bool = config("DEBUG", cast=bool, default=False)


settings = Settings()
