from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    app_name: str = "Zero Waste"

    # Database
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str
    db_url: PostgresDsn

    # OAuth JWT
    jwt_secret: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


# Only one instance of Settings for all the requests (only reads once the .env file)
@lru_cache()
def get_settings():
    return Settings()
