from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_api_key, get_db
from app import crud, models, schemas

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.get("/", response_model=List[schemas.RadPostAuth])
def read_radpostauth_all(
    db: Session = Depends(get_db), skip: int = 0, limit=100
) -> Any:
    """Retrieve all radpostauth records"""
    radpostauth = crud.radpostauth.get_multi(db=db, skip=skip, limit=limit)
    return radpostauth


@router.get("/{username}", response_model=List[schemas.RadPostAuth])
def read_radpostauth_username(
    *, db: Session = Depends(get_db), username: str, skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve all radpostauth records for a specific username"""
    radpostauth = crud.radpostauth.get_by_username(
        db=db, username=username, skip=skip, limit=limit
    )
    if not radpostauth:
        raise HTTPException(
            status_code=404, detail="No postauth records found for this Username"
        )
    return radpostauth


@router.delete("/", response_model=schemas.GenericDeleteResponse)
def delete_radpostauth_all(*, db: Session = Depends(get_db)) -> Any:
    """Deletes all radpostauth records"""
    return crud.radpostauth.remove_all(db=db)


@router.delete("/{username}", response_model=schemas.GenericDeleteResponse)
def delete_radpostauth_username(*, db: Session = Depends(get_db), username: str) -> Any:
    """Deletes all radpostauth records for a specific username"""
    return crud.radpostauth.remove_postauth_records(db=db, username=username)
