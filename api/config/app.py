from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "freeradius-bng-api"
    app_version: str = "0.0.1"
    api_token_key: str = "x-api-token"
    api_token: str
    sqlalchemy_database_url: str
    mongodb_uri: str = "mongodb://freeradius:changemeP!z@mongo:27017/"
    iana_enterprise_numbers: str = (
        "https://www.iana.org/assignments/enterprise-numbers/enterprise-numbers"
    )

    validate_avpairs: bool = False
    freeradius_dictionary_paths: list = ["/freeradius_dictionaries"]

    class Config:
        # env_file = ".env"
        fields = {
            "api_token_key": {"env": "api_token_key"},
            "api_token": {"env": "api_token"},
            "sqlalchemy_database_url": {"env": "sqlalchemy_database_url"},
            "validate_avpairs": {"env": "validate_avpairs"},
            "mongodb_uri": {"env": "mongodb_uri"},
            "iana_enterprise_numbers": {"env": "iana_enterprise_numbers"},
        }


@lru_cache()
def get_settings():
    return Settings()
