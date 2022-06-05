from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_api_key, get_db
from app import crud, models, schemas

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.post("/", response_model=schemas.RadUserGroup)
def create_radusergroup(
    *, db: Session = Depends(get_db), radusergroup_in: schemas.RadUserGroupCreate
) -> Any:
    """Create a radusergroup"""
    radusergroup = crud.radusergroup.already_exist(
        db=db, groupname=radusergroup_in.groupname, username=radusergroup_in.username
    )
    if radusergroup:
        raise HTTPException(
            status_code=400,
            detail="User Group assosication for this group and username already exist",
        )
    radusergroup = crud.radusergroup.create(db=db, obj_in=radusergroup_in)
    return radusergroup


@router.get("/", response_model=List[schemas.RadUserGroup])
def get_radusergroup_all(
    *, db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve all radusergroup assosications"""
    radusergroup = crud.radusergroup.get_multi(db=db, skip=skip, limit=limit)
    return radusergroup


@router.get("/{id}", response_model=schemas.RadUserGroup)
def get_radusergroup(*, db: Session = Depends(get_db), id: int) -> Any:
    """Retrieve a certain radusergroup assosication"""
    radusergroup = crud.radusergroup.get(db=db, id=id)
    if not radusergroup:
        raise HTTPException(
            status_code=404, detail="RadUserGroup assosication not found"
        )
    return radusergroup


@router.put("/{id}", response_model=schemas.RadUserGroup)
def update_radusergroup(
    *,
    db: Session = Depends(get_db),
    id: int,
    radusergroup_in: schemas.RadUserGroupUpdate
) -> Any:
    """Update a certain radusergroup assosication"""
    radusergroup = crud.radusergroup.get(db=db, id=id)
    if not radusergroup:
        raise HTTPException(
            status_code=404, detail="RadUserGroup assosication not found"
        )
    radusergroup = crud.radusergroup.update(
        db=db, db_obj=radusergroup, obj_in=radusergroup_in
    )
    return radusergroup


@router.delete("/{id}", response_model=schemas.RadUserGroup)
def delete_radusergroup(*, db: Session = Depends(get_db), id: int) -> Any:
    """Delete a radusergroup assosication"""
    radusergroup = crud.radusergroup.get(db=db, id=id)
    if not radusergroup:
        raise HTTPException(
            status_code=404, detail="RadUserGroup assosication not found"
        )
    radusergroup = crud.radusergroup.remove(db=db, id=id)
    return radusergroup
