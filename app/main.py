from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.api import api_router
from app.config.app import settings
from app.dependencies import async_get_db

from app.modules.vsa_logic import check_pyrad_dict, vsa_loader
from app.modules.service_logic import services_init, service_pre_checks

app = FastAPI(title="freeradius-api", openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    if settings.VALIDATE_AVPAIRS:
        attributes = check_pyrad_dict(
            settings.FREERADIUS_DICTIONARY_PATH
        )  # Check if pyrad is happy

        settings.AVPAIRS_DICT = attributes

    # Load services and perform prechecks
    services_init()
    for service in settings.SERVICES:
        await service_pre_checks(service=service)
