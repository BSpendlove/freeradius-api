from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_api_key, get_db
from app import crud, models, schemas

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.get("/", response_model=List[schemas.RadAcct])
def read_radacct_all(db: Session = Depends(get_db), skip: int = 0, limit=100) -> Any:
    """Retrieve all radacct records"""
    radacct = crud.radacct.get_multi(db=db, skip=skip, limit=limit)
    return radacct


@router.get("/{username}", response_model=List[schemas.RadAcct])
def read_radacct_username(
    *, db: Session = Depends(get_db), username: str, skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve all radacct records for a specific username"""
    radacct = crud.radacct.get_by_username(
        db=db, username=username, skip=skip, limit=limit
    )
    if not radacct:
        raise HTTPException(
            status_code=404, detail="No accounting records found for this Username"
        )
    return radacct


@router.get("/{username}", response_model=schemas.RadAcct)
def read_radacct_username_latest(
    *, db: Session = Depends(get_db), username: str
) -> Any:
    """Retrieve the latest radacct record for a specific username"""
    radacct = crud.radacct.get_last_session_by_username(db=db, username=username)
    if not radacct:
        raise HTTPException(
            status_code=404, detail="No accounting records found for this Username"
        )
    return radacct


@router.delete("/", response_model=schemas.GenericDeleteResponse)
def delete_radacct_all(*, db: Session = Depends(get_db)) -> Any:
    """Deletes all radacct records"""
    return crud.radacct.remove_accounting_records(db=db)


@router.delete("/{username}", response_model=schemas.GenericDeleteResponse)
def delete_radacct_username(*, db: Session = Depends(get_db), username: str) -> Any:
    """Deletes all radacct records for a specific username"""
    return crud.radacct.remove_accounting_records(db=db, username=username)
