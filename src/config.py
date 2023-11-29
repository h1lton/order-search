from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str

    DB_DSN: str

    DB_ECHO: bool = False

    API_ID: int
    API_HASH: str

    URL: str = "http://127.0.0.1:8000/"

    MAX_PARSED_DATETIME: timedelta = timedelta(days=7)

    ACCESS_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
