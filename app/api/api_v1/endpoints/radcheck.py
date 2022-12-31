from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import require_api_key_auth, get_db
from app import crud, models, schemas

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.RadCheck)
def create_radcheck(
    *, db: Session = Depends(get_db), radcheck_in: schemas.RadCheckCreate
) -> Any:
    """Create a radcheck attribute"""
    radcheck = crud.radcheck.already_exist(
        db=db,
        username=radcheck_in.username,
        attribute=radcheck_in.attribute,
        value=radcheck_in.value,
    )
    if radcheck:
        raise HTTPException(
            status_code=400,
            detail="Username with these attributes already exist (op value not compared)",
        )

    radcheck = crud.radcheck.create(db=db, obj_in=radcheck_in)
    return radcheck


@router.get("/", response_model=List[schemas.RadCheck])
def read_radcheck_all(db: Session = Depends(get_db), skip: int = 0, limit=100) -> Any:
    """Retrieve all radcheck attributes"""
    radcheck = crud.radcheck.get_multi(db=db, skip=skip, limit=limit)
    return radcheck


@router.get("/{id}", response_model=schemas.RadCheck)
def read_radcheck(*, db: Session = Depends(get_db), id: int) -> Any:
    """Retrieve a certain radcheck attribute"""
    radcheck = crud.radcheck.get(db=db, id=id)
    if not radcheck:
        raise HTTPException(status_code=404, detail="RadCheck not found")
    return radcheck


@router.put("/{id}", response_model=schemas.RadCheck)
def update_radcheck(
    *, db: Session = Depends(get_db), id: int, radcheck_in: schemas.RadCheckUpdate
) -> Any:
    """Update a certain radcheck attribute"""
    radcheck = crud.radcheck.get(db=db, id=id)
    if not radcheck:
        raise HTTPException(status_code=404, detail="RadCheck not found")
    radcheck = crud.radcheck.update(db=db, db_obj=radcheck, obj_in=radcheck_in)
    return radcheck


@router.delete("/{id}", response_model=schemas.RadCheck)
def delete_radcheck(*, db: Session = Depends(get_db), id: int) -> Any:
    """Delete a radcheck attribute"""
    radcheck = crud.radcheck.get(db=db, id=id)
    if not radcheck:
        raise HTTPException(status_code=404, detail="RadCheck not found")
    radcheck = crud.radcheck.remove(db=db, id=id)
    return radcheck
