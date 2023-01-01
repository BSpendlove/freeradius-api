import json
import re
from uuid import UUID
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from app.dependencies import require_api_key_auth, async_get_db
from app.config.app import settings
from app.modules.service_logic import service_user_checks
from app import schemas
import app.crud.async_driver as crud

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.Service)
async def create_user_from_service(
    create_user: schemas.ServiceCreateUser, db: AsyncSession = Depends(async_get_db)
) -> Any:
    """Creates a user based on the service"""
    user_service = None
    for service in settings.SERVICES:
        if service.service_name == create_user.service_name:
            user_service = service
            break

    if not user_service:
        raise HTTPException(
            status_code=404,
            detail=f"Service '{create_user.service_name}' is not defined in any of the service files.",
        )

    if not user_service.prechecks_passed:
        raise HTTPException(
            status_code=400,
            detail=f"Prechecks for this service have failed, please see startup logs for further information",
        )

    # Perform type checks, need to find a nicer way of doing this however I never suspect someone creating too many radius users that it causes a real production problem...
    username_types = {
        "str": "^\w+$",
        "int": "^\d+$",
        "mac_address": "^((([0-9A-Fa-f]{2}[-:.]){5}[0-9A-Fa-f]{2})|(([0-9A-Fa-f]{4}\\.){2}[0-9A-Fa-f]{4}))$",
    }
    if user_service.username_type == "regex":
        if not user_service.username_regex:
            raise HTTPException(
                status_code=400,
                detail="If a service is configured for 'username_type=regex' then you must provide a regex string to perform the match.",
            )

        regex_match = re.match(user_service.username_regex, create_user.username)
        if not regex_match:
            raise HTTPException(
                status_code=400,
                detail=f"Regex match for username is invalid for this service {user_service.service_name}",
            )
    elif user_service.username_type == "uuid":
        try:
            UUID(create_user.username)
        except:
            raise HTTPException(status_code=400, detail="Username is not a valid UUID")
    elif user_service.username_type in username_types:
        regex_match = re.match(
            username_types[user_service.username_type], create_user.username
        )

        if not regex_match:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to validate username using username_type '{user_service.username_type}'",
            )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Configured username_type ('{user_service.username_type}') for service {user_service.service_name} is not implemented",
        )

    # Map data for the pre-defined username and service in the service template
    replace_map = {
        "{{username}}": create_user.username,
        "{{service_name}}": create_user.service_name,
    }

    json_data = user_service.json()
    for k, v in replace_map.items():
        json_data = json_data.replace(k, v)

    updated_user_service = schemas.Service(**json.loads(json_data))
    user_checks_passed = await service_user_checks(
        username=create_user.username, service=updated_user_service, db=db
    )

    if not user_checks_passed:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to create user {create_user.username} due to prechecks failing",
        )

    # Auto create radgroupcheck and radgroupreply attributes
    #       Not currently implemented
    #

    # Add user to radusergroup
    if updated_user_service.radusergroups:
        for group in updated_user_service.radusergroups:
            logger.debug(f"Adding radusergroup {group}")
            await crud.radusergroup.create(db=db, obj_in=group)

    # Add user specific radcheck attributes
    if updated_user_service.radcheck_avpairs:
        for radcheck in updated_user_service.radcheck_avpairs:
            logger.debug(f"Adding radcheck {radcheck}")
            await crud.radcheck.create(db=db, obj_in=radcheck)

    # Add user specific radreply attributes
    if updated_user_service.radreply_avpairs:
        for radreply in updated_user_service.radreply_avpairs:
            logger.debug(f"Adding radreply {radreply}")
            await crud.radreply.create(db=db, obj_in=radreply)

    return updated_user_service
