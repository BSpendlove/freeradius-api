from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

from starlette.status import HTTP_403_FORBIDDEN

from app.config.app import settings
from app.database import SessionLocal

api_key_header = APIKeyHeader(name=settings.API_TOKEN_KEY, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.API_TOKEN:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
