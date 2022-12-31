from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import require_api_key_auth, get_db
from app import crud, models, schemas

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.RadGroupCheck)
def create_radgroupcheck(
    *, db: Session = Depends(get_db), radgroupcheck_in: schemas.RadGroupCheckCreate
) -> Any:
    """Create a radgroupcheck attribute"""
    radgroupcheck = crud.radgroupcheck.already_exist(
        db=db,
        groupname=radgroupcheck_in.groupname,
        attribute=radgroupcheck_in.attribute,
        value=radgroupcheck_in.value,
    )
    if radgroupcheck:
        raise HTTPException(
            status_code=400,
            detail="Group with these attributes already exist (op value not compared)",
        )
    radgroupcheck = crud.radgroupcheck.create(db=db, obj_in=radgroupcheck_in)
    return radgroupcheck


@router.get("/", response_model=List[schemas.RadGroupCheck])
def read_radgroupcheck_all(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve all radgroupcheck attributes"""
    radgroupcheck = crud.radgroupcheck.get_multi(db=db, skip=skip, limit=limit)
    return radgroupcheck


@router.get("/{id}", response_model=schemas.RadGroupCheck)
def read_radgroupcheck(*, db: Session = Depends(get_db), id: int) -> Any:
    """Retrieve a certain radgroupcheck attribute"""
    radgroupcheck = crud.radgroupcheck.get(db=db, id=id)
    if not radgroupcheck:
        raise HTTPException(status_code=404, detail="RadGroupCheck not found")
    return radgroupcheck


@router.put("/{id}", response_model=schemas.RadGroupCheck)
def update_radgroupcheck(
    *,
    db: Session = Depends(get_db),
    id: int,
    radgroupcheck_in: schemas.RadGroupCheckUpdate
) -> Any:
    """Update a certain radgroupcheck attribute"""
    radgroupcheck = crud.radgroupcheck.get(db=db, id=id)
    if not radgroupcheck:
        raise HTTPException(status_code=404, detail="RadGroupCheck not found")
    radgroupcheck = crud.radgroupcheck.update(
        db=db, db_obj=radgroupcheck, obj_in=radgroupcheck_in
    )
    return radgroupcheck


@router.delete("/{id}", response_model=schemas.RadGroupCheck)
def delete_radgroupcheck(*, db: Session = Depends(get_db), id: int) -> Any:
    """Delete a radgroupcheck attribute"""
    radgroupcheck = crud.radgroupcheck.get(db=db, id=id)
    if not radgroupcheck:
        raise HTTPException(status_code=404, detail="RadGroupCheck not found")
    radgroupcheck = crud.radgroupcheck.remove(db=db, id=id)
    return radgroupcheck
