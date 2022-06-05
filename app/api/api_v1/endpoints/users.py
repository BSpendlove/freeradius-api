from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_api_key, get_db
from app import crud, models, schemas
from app.schemas.user import RadiusUser

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.get("/", response_model=List[RadiusUser])
def get_users(*, db: Session = Depends(get_db)) -> Any:
    """Returns all the users and assosicated AVPairs + Groups"""
    # Users might exist in only the radcheck or radusergroup tables
    raise HTTPException(status_code=501, detail="Route not implemented yet")


@router.get("/{username}", response_model=RadiusUser)
def get_user(*, db: Session = Depends(get_db), username: str) -> Any:
    """Returns the specific user and assosicated AVPairs + Groups"""
    check_attributes = crud.radiususer.get_check_attributes(db=db, username=username)
    reply_attributes = crud.radiususer.get_reply_attributes(db=db, username=username)
    group_assosications = crud.radiususer.get_user_groups(db=db, username=username)

    if not check_attributes and not reply_attributes and not group_assosications:
        raise HTTPException(status_code=404, detail="Unable to find User")

    user = RadiusUser(
        username=username,
        groups=group_assosications,
        check_attributes=check_attributes,
        reply_attributes=reply_attributes,
    )
    return user
