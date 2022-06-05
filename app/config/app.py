from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    APP_NAME: str = "freeradius-bng-api"
    APP_VERSION: str = "0.1.0"
    API_TOKEN_KEY: str = "x-api-token"
    API_TOKEN: str
    SQLALCHEMY_DATABASE_URI: str
    MONGODB_DATABASE_URI: str = "mongodb://freeradius:changemeP!z@mongo:27017/"
    IANA_ENTERPRISE_NUMBERS: str = (
        "https://www.iana.org/assignments/enterprise-numbers/enterprise-numbers"
    )

    VALIDATE_AVPAIRS: bool = False
    FREERADIUS_DICTIONARY_PATHS: list = ["/freeradius_dictionaries"]

    class Config:
        # env_file = ".env"
        fields = {
            "API_TOKEN_KEY": {"env": "API_TOKEN_KEY"},
            "API_TOKEN": {"env": "API_TOKEN"},
            "SQLALCHEMY_DATABASE_URI": {"env": "SQLALCHEMY_DATABASE_URI"},
            "MONGODB_DATABASE_URI": {"env": "MONGODB_DATABASE_URI"},
            "VALIDATE_AVPAIRS": {"env": "VALIDATE_AVPAIRS"},
            "IANA_ENTERPRISE_NUMBERS": {"env": "IANA_ENTERPRISE_NUMBERS"},
        }


settings = Settings()
