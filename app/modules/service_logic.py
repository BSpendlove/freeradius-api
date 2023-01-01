import json
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from loguru import logger
from app.config.app import settings
from app.schemas.extended.service import Service
from app.database import async_local_session
from app.schemas.generic import AVPair
import app.crud.async_driver as crud


def process_cisco_avpair(av_pair: AVPair) -> AVPair:
    if av_pair.attribute.lower() != "cisco-avpair":
        logger.error("Unable to process AVPair")
        return

    av_pair_split = av_pair.value.split("=")
    if not len(av_pair_split) == 2:
        logger.error("Cisco-AVPair is not correctly formatted, should be len of 2")
        return

    return AVPair(attribute=av_pair_split[0], op="=", value=av_pair_split[1])


def services_init():
    """Initializes JSON defined services and prepares them to be checked"""
    service_files = Path(settings.SERVICES_DIRECTORY)

    if not service_files.is_dir():
        logger.info(
            "Unable to find any services to load, normal endpoints will still work as expected."
        )
        return

    services = []

    for file in service_files.iterdir():
        if file.suffix != ".json":
            continue

        with file.open() as service_file:
            try:
                data = json.load(service_file)
            except:
                logger.error(
                    f"Unable to load services in {file.name}, skipping this file..."
                )
                continue

            if isinstance(data, list):
                for entry in data:
                    services.append(entry)
            else:
                services.append(data)

    for service in services:
        try:
            service = Service(**service)
        except Exception as error:
            logger.error(
                f"Unable to load service {service.get('service_name')} due to error:\n{error}. Skipping..."
            )
            continue

        if service.service_name in settings.SERVICES:
            logger.error(
                f"This service ({service.service_name}) has already been defined, please ensure services are not duplicated and have unique service_names. Skipping"
            )
            continue

        settings.SERVICES.append(service)
        logger.success(f"Added service {service.service_name}")

    return settings.SERVICES


async def service_user_checks(
    username: str, service: Service, db: AsyncSession
) -> bool:
    """Performs checks for the radcheck_avpair and radreply_avpair parts of a Service

    Args:
        username:       Username of the User
        service:        Service
        db:             DB session passed from the FastAPI dependency
    """
    logger.info(
        f"Performing prechecks on user '{username}' for service '{service.service_name}'"
    )
    if not service.radcheck_avpairs or not service.radreply_avpairs:
        return True

    # RadCheck
    for avpair in service.radcheck_avpairs:
        if avpair.username == "{{username}}":
            avpair.username == username

        if settings.VALIDATE_AVPAIRS and avpair.attribute.lower() == "cisco-avpair":
            cisco_avpair = process_cisco_avpair(av_pair=avpair)
            existing_avpairs = await crud.radcheck.get_avpair_value_like(
                db=db,
                username=avpair.username,
                attribute=avpair.attribute,
                expr=f"{cisco_avpair.attribute}{cisco_avpair.op}",
            )
        else:
            existing_avpairs = await crud.radcheck.already_exist(
                db=db,
                username=avpair.username,
                attribute=avpair.attribute,
                value=avpair.value,
            )

        if existing_avpairs:
            logger.warning(
                f"Detected existing RadCheck AVPair {avpair.attribute} for username {username}"
            )
            return False

    # RadReply
    for avpair in service.radreply_avpairs:
        if avpair.username == "{{username}}":
            avpair.username == username

        if settings.VALIDATE_AVPAIRS and avpair.attribute.lower() == "cisco-avpair":
            cisco_avpair = process_cisco_avpair(av_pair=avpair)
            existing_avpairs = await crud.radreply.get_avpair_value_like(
                db=db,
                username=avpair.username,
                attribute=avpair.attribute,
                expr=f"{cisco_avpair.attribute}{cisco_avpair.op}",
            )
        else:
            existing_avpairs = await crud.radreply.already_exist(
                db=db,
                username=avpair.username,
                attribute=avpair.attribute,
                value=avpair.value,
            )

        if existing_avpairs:
            logger.warning(
                f"Detected existing RadReply AVPair {avpair.attribute} for username {username}"
            )
            return False

    return True


async def service_pre_checks(
    service: Service, async_session: AsyncSession = async_local_session
) -> bool:
    """Performs checks to ensure any groups are created and synced with the defined service

    If a service is amended during the lifecycle, the user must ensure that existing entries in the database
    are amended to meet the new service configuration, this application will not attempt to clean up database
    entries to prevent accidental deletion/updates of database records.

    A service is allowed to be called after prechecks_passed is set to True which can only happen when the following
    conditions are met:

        - All RadGroupCheck attributes exist in the database (compares Attribute, Op, Value)
        - All RadGroupReply attributes exist in the database (compares Attribute, Op, Value)

    Args:
        service:        Service
    """
    logger.info(f"Performing prechecks on service '{service.service_name}'")
    async with async_session() as db:
        # Check if service has a group and all related attributes are populated in the database
        # RadGroupCheck
        if service.radgroupcheck_avpairs:
            for avpair in service.radgroupcheck_avpairs:
                if avpair.groupname == "{{service_name}}":
                    avpair.groupname = service.service_name

                radgroupcheck_av_exist = await crud.radgroupcheck.already_exist_strict(
                    db=db,
                    groupname=avpair.groupname,
                    attribute=avpair.attribute,
                    op=avpair.op,
                    value=avpair.value,
                )

                if not radgroupcheck_av_exist:
                    logger.warning(
                        f"Service {service.service_name}: RadGroupCheck AVPair: '{avpair.attribute} {avpair.op} {avpair.value}' does not exist in the database"
                    )
                    return False

        # RadGroupReply
        if service.radgroupreply_avpairs:
            for avpair in service.radgroupreply_avpairs:
                if avpair.groupname == "{{service_name}}":
                    avpair.groupname = service.service_name

                radgroupreply_av_exist = await crud.radgroupreply.already_exist_strict(
                    db=db,
                    groupname=avpair.groupname,
                    attribute=avpair.attribute,
                    op=avpair.op,
                    value=avpair.value,
                )

                if not radgroupreply_av_exist:
                    logger.warning(
                        f"Service {service.service_name}: RadGroupReply AVPair: '{avpair.attribute} {avpair.op} {avpair.value}' does not exist in the database"
                    )
                    return False

    logger.success(f"Service {service.service_name} pre-checks passed!")
    service.prechecks_passed = True
    return True
