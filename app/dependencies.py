from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

from starlette.status import HTTP_403_FORBIDDEN
from loguru import logger

from app.config.app import settings
from app.database import SessionLocal

api_key_header = APIKeyHeader(name=settings.API_TOKEN_KEY, auto_error=False)


def require_api_key_auth(api_key: str = Security(api_key_header)):
    if api_key not in settings.API_TOKENS:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    logger.debug("API Key authenticated")
    return True


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
