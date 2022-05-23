from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..config.app import Settings, get_settings
from ..modules.mongo import Mongo
from ..dependencies import get_api_key, get_db
from ..crud import create, read, update, delete
from ..schemas import (
    RadiusAttribute,
    RadiusAttributeDelete,
    RadiusUser,
    RadiusUserCreate,
    RadiusAttributeCreate,
)
from loguru import logger

router = APIRouter(
    prefix="/api/v1/radius/users",
    dependencies=[Depends(get_api_key)],
    tags=["Users"],
)


@router.get("/", response_model=List[RadiusUser])
def get_radius_users(db: Session = Depends(get_db)):
    users = read.users(db)
    if not users:
        raise HTTPException(
            status_code=404, detail="No Users are configured with individual attributes"
        )
    return users


@router.get("/{username}", response_model=RadiusUser)
def get_radius_user(
    username: str,
    db: Session = Depends(get_db),
):
    user = read.user(db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/", response_model=RadiusUser)
def create_radius_user(user: RadiusUserCreate, db: Session = Depends(get_db)):
    existing_user = read.user(db, username=user.username)

    if existing_user:
        raise HTTPException(status_code=404, detail="User already exist")

    group_exist = read.group(db, groupname=user.groupname)
    if group_exist is None:
        raise HTTPException(status_code=404, detail="Group does not exist")

    user = create.user(db=db, user=user)
    if user is None:
        raise HTTPException(status_code=404, detail="Unable to create User")

    return user


@router.delete("/{username}")
def delete_radius_user(username: str, db: Session = Depends(get_db)):
    existing_user = read.user(db, username=username)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="Unable to find User to delete")

    return {"deleted_rows": delete.user(db, username=username)}


@router.post("/{username}/attribute/check", response_model=RadiusUser)
def create_radius_user_attribute_check(
    username: str,
    attribute: RadiusAttributeCreate,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    existing_user = read.user(db, username=username)
    if existing_user is None:
        raise HTTPException(
            status_code=404, detail="Unable to find user to add attribute"
        )

    if settings.validate_avpairs:
        mongo = Mongo(uri=settings.mongodb_uri)
        mongo.setup_mongodb()

        attribute_exist = mongo.db.attributes.find_one(
            {"attribute_name": attribute.attribute}
        )

        if not attribute_exist:
            logger.error(f"Attribute does not exist {attribute.attribute}")
            raise HTTPException(
                status_code=404,
                detail="Unable to validate attribute pair because it doesn't exist in the Validation database",
            )

    for group in existing_user.radusergroup:
        for existing_group_attribute in read.group_check_attributes(
            db=db, groupname=group.groupname
        ):
            if (
                existing_group_attribute.attribute == attribute.attribute
                and existing_group_attribute.value == attribute.value
            ):
                raise HTTPException(
                    status_code=404,
                    detail="AVPair already used in a Group assigned to this User",
                )

    for existing_attribute in existing_user.radcheck:
        if (
            existing_attribute.attribute == attribute.attribute
            and existing_attribute.value == attribute.value
        ):
            raise HTTPException(
                status_code=404,
                detail="AVPair already present for this User",
            )

    user = create.user_check_attribute(db=db, user=existing_user, attribute=attribute)

    return user


@router.delete("/{username}/attribute/check")
def delete_radius_user_attribute_check(
    username: str, attribute: RadiusAttributeDelete, db: Session = Depends(get_db)
):
    existing_user = read.user(db, username=username)
    if existing_user is None:
        raise HTTPException(
            status_code=404, detail="Unable to find user to Delete attribute"
        )

    return {
        "deleted_rows": delete.user_check_attribute(
            db=db, user=existing_user, attribute=attribute
        )
    }


@router.post("/{username}/attribute/reply", response_model=RadiusUser)
def create_radius_user_attribute_reply(
    username: str,
    attribute: RadiusAttributeCreate,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    existing_user = read.user(db, username=username)
    if existing_user is None:
        raise HTTPException(
            status_code=404, detail="Unable to find user to add attribute"
        )

    if settings.validate_avpairs:
        mongo = Mongo(uri=settings.mongodb_uri)
        mongo.setup_mongodb()

        attribute_exist = mongo.db.attributes.find_one(
            {"attribute_name": attribute.attribute}
        )

        if not attribute_exist:
            raise HTTPException(
                status_code=404,
                detail="Unable to validate attribute pair because it doesn't exist in the Validation database",
            )

    for group in existing_user.radusergroup:
        for existing_group_attribute in read.group_reply_attributes(
            db=db, groupname=group.groupname
        ):
            if (
                existing_group_attribute.attribute == attribute.attribute
                and existing_group_attribute.value == attribute.value
            ):
                raise HTTPException(
                    status_code=404,
                    detail="AVPair already used in a Group assigned to this User",
                )

    for existing_attribute in existing_user.radreply:
        if (
            existing_attribute.attribute == attribute.attribute
            and existing_attribute.value == attribute.value
        ):
            raise HTTPException(
                status_code=404,
                detail="AVPair already present for this User",
            )

    user = create.user_reply_attribute(db=db, user=existing_user, attribute=attribute)
    return user


@router.delete("/{username}/attribute/reply")
def delete_radius_user_attribute_reply(
    username: str, attribute: RadiusAttributeDelete, db: Session = Depends(get_db)
):
    existing_user = read.user(db, username=username)
    if existing_user is None:
        raise HTTPException(
            status_code=404, detail="Unable to find user to Delete attribute"
        )

    return {
        "deleted_rows": delete.user_reply_attribute(
            db=db, user=existing_user, attribute=attribute
        )
    }
