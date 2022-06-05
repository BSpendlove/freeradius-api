from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_api_key, get_db
from app import crud, models, schemas

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.post("/", response_model=schemas.NAS)
def create_nas(*, db: Session = Depends(get_db), nas_in: schemas.NASCreate) -> Any:
    """Create a NAS client"""
    nas = crud.nas.already_exist(db=db, nasname=nas_in.nasname, server=nas_in.server)
    if nas:
        raise HTTPException(
            status_code=400, detail="NAS client with these attributes already exist"
        )
    nas = crud.nas.create(db=db, obj_in=nas_in)
    return nas


@router.get("/", response_model=List[schemas.NAS])
def read_nas_all(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """Retrieve all NAS clients"""
    nas = crud.nas.get_multi(db=db, skip=skip, limit=limit)
    return nas


@router.get("/{id}", response_model=schemas.NAS)
def rad_nas(*, db: Session = Depends(get_db), id: int) -> Any:
    """Retrieve a certain NAS client"""
    nas = crud.nas.get(db=db, id=id)
    if not nas:
        raise HTTPException(status_code=404, detail="NAS client not found")
    return nas


@router.put("/{id}", response_model=schemas.NAS)
def update_nas(
    *, db: Session = Depends(get_db), id: int, nas_in: schemas.NASUpdate
) -> Any:
    """Update a certain NAS client"""
    nas = crud.nas.get(db=db, id=id)
    if not nas:
        raise HTTPException(status_code=404, detail="NAS client not found")
    nas = crud.nas.update(db=db, db_obj=nas, obj_in=nas_in)
    return nas


@router.delete("/{id}", response_model=schemas.NAS)
def delete_nas(*, db: Session = Depends(get_db), id: int) -> Any:
    """Delete a NAS client"""
    nas = crud.nas.get(db=db, id=id)
    if not nas:
        raise HTTPException(status_code=404, detail="NAS client not found")
    nas = crud.nas.remove(db=db, id=id)
    return nas
