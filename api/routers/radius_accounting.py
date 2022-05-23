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
    RadiusUserAccounting,
    RadiusUserCreate,
    RadiusAttributeCreate,
)

router = APIRouter(
    prefix="/api/v1/radius/accounting",
    dependencies=[Depends(get_api_key)],
    tags=["Accounting"],
)


@router.get("/", response_model=List[RadiusUserAccounting])
def get_radius_accounting(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    accounting = read.accounting(db=db, skip=skip, limit=limit)
    return accounting


@router.delete("/")
def delete_radius_accounting(db: Session = Depends(get_db)):
    return {"deleted_rows": delete.accounting(db=db)}


@router.get("/{username}", response_model=List[RadiusUserAccounting])
def get_radius_accounting_username(
    username: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    accounting_user = read.accounting_user(
        db=db, username=username, skip=skip, limit=limit
    )
    return accounting_user


@router.delete("/{username}")
def delete_radius_accounting_username(username: str, db: Session = Depends(get_db)):
    return {"deleted_rows": delete.accounting_user(db=db, username=username)}
