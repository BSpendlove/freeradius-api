from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    APP_NAME: str = "freeradius-bng-api"
    APP_VERSION: str = "0.1.0"
    API_TOKEN_KEY: str = "x-api-token"
    API_TOKENS: list = [
        "change-me-please",  # Key for User #1
        "some-other-key",  # API Key for User #2
    ]
    SQLALCHEMY_DATABASE_URI: str = "mysql+pymysql://radius_write:radius_write@localhost:4006/radius?charset=utf8mb4"

    VALIDATE_AVPAIRS: bool = False
    FREERADIUS_DICTIONARY_PATH: str = "/freeradius_dictionaries/dictionary"
    AVPAIRS_DICT: dict = {}


settings = Settings()
