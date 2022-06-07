from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    APP_NAME: str = "freeradius-bng-api"
    APP_VERSION: str = "0.1.0"
    API_TOKEN_KEY: str = "x-api-token"
    API_TOKEN: str
    SQLALCHEMY_DATABASE_URI: str

    VALIDATE_AVPAIRS: bool = True
    FREERADIUS_DICTIONARY_PATH: str = "/freeradius_dictionaries/dictionary"
    AVPAIRS_DICT: dict = {}

    class Config:
        fields = {
            "API_TOKEN_KEY": {"env": "API_TOKEN_KEY"},
            "API_TOKEN": {"env": "API_TOKEN"},
            "SQLALCHEMY_DATABASE_URI": {"env": "SQLALCHEMY_DATABASE_URI"},
            "VALIDATE_AVPAIRS": {"env": "VALIDATE_AVPAIRS"},
        }


settings = Settings()
