from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.dependencies import get_api_key, get_db
from app import crud, models, schemas

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.post("/", response_model=schemas.RadiusGroup)
def create_group(
    *, db: Session = Depends(get_db), group_in: schemas.RadiusGroupCreate
) -> Any:
    """Create a Group with the assosicated AVPairs"""
    existing_group = crud.radiusgroup.get_by_groupname(
        db=db, groupname=group_in.groupname
    )
    if existing_group:
        raise HTTPException(status_code=400, detail=f"Group already exist")

    if (
        not group_in.check_attributes
        and not group_in.reply_attributes
        and not group_in.users
    ):
        raise HTTPException(
            status_code=400,
            detail="Group must contain at least 1 user or 1 check/reply attribute mapping",
        )

    try:
        # Add attributes to radgroupcheck table
        for check_attribute in group_in.check_attributes:
            check_json = jsonable_encoder(check_attribute)
            check_obj = schemas.RadGroupCheck(
                groupname=group_in.groupname, **check_json
            )
            crud.radgroupcheck.create(db=db, obj_in=check_obj)

        # Add attributes to radreply table
        for reply_attribute in group_in.reply_attributes:
            reply_json = jsonable_encoder(reply_attribute)
            reply_obj = schemas.RadGroupReply(
                groupname=group_in.groupname, **reply_json
            )
            crud.radgroupreply.create(db=db, obj_in=reply_obj)

        # Add attributes to radusergroup table
        for user in group_in.users:
            user_json = jsonable_encoder(user)
            user_obj = schemas.RadUserGroup(groupname=group_in.groupname, **user_json)
            crud.radusergroup.create(db=db, obj_in=user_obj)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error attempting to add the group to the database. Error: {error}",
        )

    response = crud.radiusgroup.get_by_groupname(db=db, groupname=group_in.groupname)
    return response


@router.get("/", response_model=List[schemas.RadiusGroup])
def get_groups(*, db: Session = Depends(get_db)) -> Any:
    """Returns all the groups and assosicated AVPairs + Users"""
    # Groups might exist in only the radgroupcheck or radgroupreply tables
    raise HTTPException(status_code=501, detail="Route not implemented yet")


@router.get("/{groupname}", response_model=schemas.RadiusGroup)
def get_group(*, db: Session = Depends(get_db), groupname: str) -> Any:
    """Returns the specific group and assosicated AVPairs + Users"""
    group_check_attributes = crud.radiusgroup.get_check_attributes(
        db=db, groupname=groupname
    )
    group_reply_attributes = crud.radiusgroup.get_reply_attributes(
        db=db, groupname=groupname
    )
    group_users = crud.radiusgroup.get_users(db=db, groupname=groupname)

    if not group_check_attributes and not group_reply_attributes and not group_users:
        raise HTTPException(status_code=404, detail="Unable to find Group")

    group = schemas.RadiusGroup(
        groupname=groupname,
        users=group_users,
        check_attributes=group_check_attributes,
        reply_attributes=group_reply_attributes,
    )
    return group


@router.delete("/{groupname}", response_model=schemas.GenericDeleteResponse)
def delete_group(*, db: Session = Depends(get_db), groupname: str) -> Any:
    """Deletes the specific group and assosicated AVPairs + assosicated user group mappings"""
    rows_deleted = crud.radiusgroup.remove_from_all_tables(db=db, groupname=groupname)

    response = schemas.GenericDeleteResponse(rows_deleted=rows_deleted)
    return response
