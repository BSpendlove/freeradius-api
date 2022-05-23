from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_api_key, get_db
from ..crud import create, read, update, delete
from ..schemas import (
    RadiusAttribute,
    RadiusAttributeDelete,
    RadiusPostAuthentication,
    RadiusUser,
    RadiusUserCreate,
    RadiusAttributeCreate,
)

router = APIRouter(
    prefix="/api/v1/radius/postauth",
    dependencies=[Depends(get_api_key)],
    tags=["PostAuth"],
)


@router.get("/", response_model=List[RadiusPostAuthentication])
def get_radius_postauth(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    postauth = read.postauth(db=db, skip=skip, limit=limit)
    return postauth


@router.delete("/")
def delete_radius_postauth(db: Session = Depends(get_db)):
    return {"deleted_rows": delete.postauth(db=db)}


@router.get("/{username}", response_model=List[RadiusPostAuthentication])
def get_radius_postauth_username(
    username: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    postauth = read.postauth_user(db=db, username=username, skip=skip, limit=limit)
    return postauth


@router.delete("/{username}")
def delete_radius_postauth_username(username: str, db: Session = Depends(get_db)):
    return {"deleted_rows": delete.postauth_user(db=db, username=username)}
