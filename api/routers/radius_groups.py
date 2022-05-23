from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.config.app import get_settings, Settings

from ..dependencies import get_api_key, get_db
from ..modules.mongo import Mongo
from ..crud import create, read, update, delete
from ..schemas import (
    RadiusAttributeCreate,
    RadiusAttributeDelete,
    RadiusGroup,
    RadiusGroupCreate,
    RadiusGroupDelete,
)

router = APIRouter(
    prefix="/api/v1/radius/groups",
    dependencies=[Depends(get_api_key)],
    tags=["Groups"],
)


@router.get("/", response_model=List[RadiusGroup])
def get_radius_groups(db: Session = Depends(get_db)):
    groups = read.groups(db)
    if groups is None:
        raise HTTPException(status_code=404, detail="No Groups exist")
    return groups


@router.get("/{groupname}", response_model=RadiusGroup)
def get_radius_group(groupname: str, db: Session = Depends(get_db)):
    group = read.group(db, groupname)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    return group


@router.post("/", response_model=RadiusGroup)
def create_radius_group(group: RadiusGroupCreate, db: Session = Depends(get_db)):
    existing_group = read.group(db=db, groupname=group.groupname)

    if existing_group:
        raise HTTPException(status_code=404, detail="Group already exist")

    group = create.group(db=db, group=group)
    if group is None:
        raise HTTPException(status_code=404, detail="Unable to create Group")

    return group


@router.delete("/{groupname}")
def delete_radius_group(groupname: str, db: Session = Depends(get_db)):
    existing_group = read.group(db=db, groupname=groupname)

    if existing_group is None:
        raise HTTPException(status_code=404, detail="Group does not exist")

    if existing_group.radusergroup:
        raise HTTPException(
            status_code=404, detail="Unable to delete Group that have users in"
        )

    return {"deleted_rows": delete.group(db=db, groupname=groupname)}


@router.post("/{groupname}/attribute/check", response_model=RadiusGroup)
def create_radius_group_attribute_check(
    groupname: str,
    attribute: RadiusAttributeCreate,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    existing_group = read.group(db=db, groupname=groupname)

    if existing_group is None:
        raise HTTPException(status_code=404, detail="Group does not exist")

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

    for existing_attribute in existing_group.radgroupcheck:
        if (
            existing_attribute.attribute == attribute.attribute
            and existing_attribute.value == attribute.value
        ):
            raise HTTPException(
                status_code=404, detail="AVPair already present for this Group"
            )

    group = create.group_check_attribute(
        db=db, group=existing_group, attribute=attribute
    )
    return group


@router.delete("/{groupname}/attribute/check")
def delete_radius_group_attribute_check(
    groupname: str, attribute: RadiusAttributeDelete, db: Session = Depends(get_db)
):
    existing_group = read.group(db, groupname=groupname)
    if existing_group is None:
        raise HTTPException(
            status_code=404, detail="Unable to find Group to Delete attribute"
        )

    return {
        "deleted_rows": delete.group_check_attribute(
            db=db, group=existing_group, attribute=attribute
        )
    }


@router.post("/{groupname}/attribute/reply", response_model=RadiusGroup)
def create_radius_group_attribute_reply(
    groupname: str,
    attribute: RadiusAttributeCreate,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    existing_group = read.group(db, groupname=groupname)
    if existing_group is None:
        raise HTTPException(
            status_code=404, detail="Unable to find Group to add attribute"
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

    for existing_attribute in existing_group.radgroupreply:
        if (
            existing_attribute.attribute == attribute.attribute
            and existing_attribute.value == attribute.value
        ):
            raise HTTPException(
                status_code=404,
                detail="AVPair already present for this group",
            )

    group = create.group_reply_attribute(
        db=db, group=existing_group, attribute=attribute
    )
    return group


@router.delete("/{groupname}/attribute/reply")
def delete_radius_group_attribute_reply(
    groupname: str, attribute: RadiusAttributeDelete, db: Session = Depends(get_db)
):
    existing_group = read.group(db, groupname=groupname)
    if existing_group is None:
        raise HTTPException(
            status_code=404, detail="Unable to find group to Delete attribute"
        )

    return {
        "deleted_rows": delete.group_reply_attribute(
            db=db, group=existing_group, attribute=attribute
        )
    }
