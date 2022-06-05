from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_api_key, get_db
from app import crud, models, schemas
from app.schemas.group import RadiusGroup

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.get("/", response_model=List[RadiusGroup])
def get_groups(*, db: Session = Depends(get_db)) -> Any:
    """Returns all the groups and assosicated AVPairs + Users"""
    # Groups might exist in only the radgroupcheck or radgroupreply tables
    raise HTTPException(status_code=501, detail="Route not implemented yet")


@router.get("/{groupname}", response_model=RadiusGroup)
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

    group = RadiusGroup(
        groupname=groupname,
        users=group_users,
        check_attributes=group_check_attributes,
        reply_attributes=group_reply_attributes,
    )
    return group
