from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import require_api_key_auth, get_db
from app import crud, models, schemas

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.RadGroupReply)
def create_radgroupreply(
    *, db: Session = Depends(get_db), radgroupreply_in: schemas.RadGroupReplyCreate
) -> Any:
    """Create a radgroupreply attribute"""
    radgroupreply = crud.radgroupreply.already_exist(
        db=db,
        groupname=radgroupreply_in.groupname,
        attribute=radgroupreply_in.attribute,
        value=radgroupreply_in.value,
    )
    if radgroupreply:
        raise HTTPException(
            status_code=400,
            detail="Group with these attributes already exist (op value not compared)",
        )
    radgroupreply = crud.radgroupreply.create(db=db, obj_in=radgroupreply_in)
    return radgroupreply


@router.get("/", response_model=List[schemas.RadGroupReply])
def read_radgroupreply_all(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve all radgroupreply attributes"""
    radgroupreply = crud.radgroupreply.get_multi(db=db, skip=skip, limit=limit)
    return radgroupreply


@router.get("/{id}", response_model=schemas.RadGroupReply)
def read_radgroupreply(*, db: Session = Depends(get_db), id: int) -> Any:
    """Retrieve a certain radgroupreply attribute"""
    radgroupreply = crud.radgroupreply.get(db=db, id=id)
    if not radgroupreply:
        raise HTTPException(status_code=404, detail="RadGroupReply not found")
    return radgroupreply


@router.put("/{id}", response_model=schemas.RadGroupReply)
def update_radgroupreply(
    *,
    db: Session = Depends(get_db),
    id: int,
    radgroupreply_in: schemas.RadGroupReplyUpdate
) -> Any:
    """Update a certain radgroupreply attribute"""
    radgroupreply = crud.radgroupreply.get(db=db, id=id)
    if not radgroupreply:
        raise HTTPException(status_code=404, detail="RadGroupReply not found")
    radgroupreply = crud.radgroupreply.update(
        db=db, db_obj=radgroupreply, obj_in=radgroupreply_in
    )
    return radgroupreply


@router.delete("/{id}", response_model=schemas.RadGroupReply)
def delete_radgroupreply(*, db: Session = Depends(get_db), id: int) -> Any:
    """Delete a radgroupreply attribute"""
    radgroupreply = crud.radgroupreply.get(db=db, id=id)
    if not radgroupreply:
        raise HTTPException(status_code=404, detail="RadGroupReply not found")
    radgroupreply = crud.radgroupreply.remove(db=db, id=id)
    return radgroupreply
