import os
from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    app_name: str = "Zero Waste"
    fastapi_env: str = "development"

    # Database
    db_host: str = None
    db_port: str = None
    db_name: str = None
    db_user: str = None
    db_password: str = None
    db_url: PostgresDsn = None

    # OAuth JWT
    jwt_secret: str = None
    access_token_expire_minutes: int = 0

    class Config:
        env_file = ".env"


class TestSettings(BaseSettings):
    fastapi_env = "testing"

    # Database
    db_url: PostgresDsn = "postgresql+asyncpg://zw:zw@zw-db:5432/zw_test"


# Only one instance of Settings for all the requests (only reads once the .env file)
@lru_cache()
def get_settings():
    if os.getenv("FASTAPI_ENV") == "testing":
        return TestSettings()
    return Settings()
