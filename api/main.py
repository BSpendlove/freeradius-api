from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey
from loguru import logger

from .config.app import Settings, get_settings
from .modules.mongo import Mongo

settings = get_settings()

if settings.validate_avpairs:
    logger.debug(
        "validate_avpairs is True, will validate existing FreeRADIUS dictionary paths"
    )

    logger.debug(settings)
    # Add Attributes and Values to Database for Validation Logic if enabled
    from .modules.iana import get_iana_numbers
    from .modules.vsa_logic import vsa_loader

    # iana_numbers = get_iana_numbers()
    # Add logic to insert into iana_vendor

    # Mongo
    mongo = Mongo(uri=settings.mongodb_uri)
    try:
        mongo.setup_mongodb()
        mongo.client.server_info()
    except:
        raise Exception(
            "Unable to get server info, is mongodb server reachable? mongodb server must be reachable to use 'validate_avpairs'"
        )

    # Add VSAs to MongoDB
    vsas = vsa_loader(paths=settings.freeradius_dictionary_paths)
    mongo.create_vsa_mappings(vsas=vsas)

from .dependencies import get_api_key

from .routers import radius_users, radius_groups, radius_postauth, radius_accounting

app = FastAPI()

# Register Routers
app.include_router(radius_users.router)
app.include_router(radius_groups.router)
app.include_router(radius_postauth.router)
app.include_router(radius_accounting.router)


@app.get("/version")
async def get_version(api_key: APIKey = Depends(get_api_key)):
    return {"error": False, "version": get_settings().app_version}
