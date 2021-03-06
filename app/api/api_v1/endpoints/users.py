from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.dependencies import get_api_key, get_db
from app import crud, models, schemas

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.post("/", response_model=schemas.RadiusUser)
def create_user(
    *, db: Session = Depends(get_db), user_in: schemas.RadiusUserCreate
) -> Any:
    """Create a User with the assosicated AVPairs + Groups"""
    existing_user = crud.radiususer.get_by_username(db=db, username=user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail=f"User already exist")

    if (
        not user_in.check_attributes
        and not user_in.reply_attributes
        and not user_in.groups
    ):
        raise HTTPException(
            status_code=400,
            detail=f"User should at least be apart of 1 group or have 1 check or reply attribute assigned",
        )

    try:
        # Add attributes to radcheck table
        for check_attribute in user_in.check_attributes:
            check_json = jsonable_encoder(check_attribute)
            check_obj = schemas.RadCheck(username=user_in.username, **check_json)
            crud.radcheck.create(db=db, obj_in=check_obj)

        # Add attributes to radreply table
        for reply_attribute in user_in.reply_attributes:
            reply_json = jsonable_encoder(reply_attribute)
            reply_obj = schemas.RadReply(username=user_in.username, **reply_json)
            crud.radreply.create(db=db, obj_in=reply_obj)

        # Add attributes to radusergroup table
        for group in user_in.groups:
            group_json = jsonable_encoder(group)
            group_obj = schemas.RadUserGroup(username=user_in.username, **group_json)
            crud.radusergroup.create(db=db, obj_in=group_obj)

    except Exception as error:
        raise HTTPException(
            status_code=501,
            detail=f"Error attempting to add the user to the database. Error: {error}",
        )

    response = crud.radiususer.get_by_username(db=db, username=user_in.username)
    return response


@router.get("/", response_model=List[schemas.RadiusUser])
def get_users(*, db: Session = Depends(get_db)) -> Any:
    """Returns all the users and assosicated AVPairs + Groups"""
    # Users might exist in only the radcheck or radusergroup tables
    raise HTTPException(status_code=501, detail="Route not implemented yet")


@router.get("/{username}", response_model=schemas.RadiusUser)
def get_user(*, db: Session = Depends(get_db), username: str) -> Any:
    """Returns the specific user and assosicated AVPairs + Groups"""
    check_attributes = crud.radiususer.get_check_attributes(db=db, username=username)
    reply_attributes = crud.radiususer.get_reply_attributes(db=db, username=username)
    group_assosications = crud.radiususer.get_user_groups(db=db, username=username)

    if not check_attributes and not reply_attributes and not group_assosications:
        raise HTTPException(status_code=404, detail="Unable to find User")

    user = schemas.RadiusUser(
        username=username,
        groups=group_assosications,
        check_attributes=check_attributes,
        reply_attributes=reply_attributes,
    )
    return user


@router.delete("/{username}", response_model=schemas.GenericDeleteResponse)
def delete_user(
    *,
    db: Session = Depends(get_db),
    username: str,
    include_acct: bool = False,
    include_postauth: bool = False,
) -> Any:
    """Deletes the specific user and assosicated AVPairs + Group assosications"""
    rows_deleted = crud.radiususer.remove_from_all_tables(
        db=db,
        username=username,
        include_acct=include_acct,
        include_postauth=include_postauth,
    )

    response = schemas.GenericDeleteResponse(rows_deleted=rows_deleted)
    return response
