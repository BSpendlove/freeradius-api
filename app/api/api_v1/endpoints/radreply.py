from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import require_api_key_auth, get_db
from app import crud, models, schemas

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.RadReply)
def create_radreply(
    *, db: Session = Depends(get_db), radreply_in: schemas.RadReplyCreate
) -> Any:
    """Create a radreply attribute"""
    radreply = crud.radreply.already_exist(
        db=db,
        username=radreply_in.username,
        attribute=radreply_in.attribute,
        value=radreply_in.value,
    )
    if radreply:
        raise HTTPException(
            status_code=400,
            detail="Username with these attributes already exist (op value not compared)",
        )

    radreply = crud.radreply.create(db=db, obj_in=radreply_in)
    return radreply


@router.get("/", response_model=List[schemas.RadReply])
def read_radreply_all(db: Session = Depends(get_db), skip: int = 0, limit=100) -> Any:
    """Retrieve all radreply attributes."""
    radreply = crud.radreply.get_multi(db=db, skip=skip, limit=limit)
    return radreply


@router.get("/{id}", response_model=schemas.RadReply)
def read_radreply(*, db: Session = Depends(get_db), id: int) -> Any:
    """Retrieve a certain radreply attribute"""
    radreply = crud.radreply.get(db=db, id=id)
    if not radreply:
        raise HTTPException(status_code=404, detail="RadReply not found")
    return radreply


@router.put("/{id}", response_model=schemas.RadReply)
def update_radreply(
    *, db: Session = Depends(get_db), id: int, radreply_in: schemas.RadReplyUpdate
) -> Any:
    """Update a certain radreply attribute"""
    radreply = crud.radreply.get(db=db, id=id)
    if not radreply:
        raise HTTPException(status_code=404, detail="RadReply not found")
    radreply = crud.radreply.update(db=db, db_obj=radreply, obj_in=radreply_in)
    return radreply


@router.delete("/{id}", response_model=schemas.RadReply)
def delete_radreply(*, db: Session = Depends(get_db), id: int) -> Any:
    """Delete a radreply attribute"""
    radreply = crud.radreply.get(db=db, id=id)
    if not radreply:
        raise HTTPException(status_code=404, detail="RadReply not found")
    radreply = crud.radreply.remove(db=db, id=id)
    return radreply
