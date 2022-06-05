from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.config.app import settings

from app.modules.vsa_logic import check_pyrad_dict, vsa_loader

app = FastAPI(title="freeradius-api", openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
def startup_event():
    if settings.VALIDATE_AVPAIRS:
        attributes = check_pyrad_dict(
            settings.FREERADIUS_DICTIONARY_PATH
        )  # Check if pyrad is happy

        settings.AVPAIRS_DICT = attributes
