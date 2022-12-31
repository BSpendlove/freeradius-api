from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import require_api_key_auth, async_get_db
from app import schemas
import app.crud.async_driver as crud

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.RadUserGroup)
async def create_radusergroup(
    *,
    db: AsyncSession = Depends(async_get_db),
    radusergroup_in: schemas.RadUserGroupCreate
) -> Any:
    """Create a radusergroup"""
    radusergroup = await crud.radusergroup.already_exist(
        db=db, groupname=radusergroup_in.groupname, username=radusergroup_in.username
    )
    if radusergroup:
        raise HTTPException(
            status_code=400,
            detail="User Group assosication for this group and username already exist",
        )
    radusergroup = await crud.radusergroup.create(db=db, obj_in=radusergroup_in)
    return radusergroup


@router.get("/", response_model=List[schemas.RadUserGroup])
async def get_radusergroup_all(
    *, db: AsyncSession = Depends(async_get_db), skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve all radusergroup assosications"""
    radusergroup = await crud.radusergroup.get_multi(db=db, skip=skip, limit=limit)
    return radusergroup


@router.get("/{id}", response_model=schemas.RadUserGroup)
async def get_radusergroup(*, db: AsyncSession = Depends(async_get_db), id: int) -> Any:
    """Retrieve a certain radusergroup assosication"""
    radusergroup = await crud.radusergroup.get(db=db, id=id)
    if not radusergroup:
        raise HTTPException(
            status_code=404, detail="RadUserGroup assosication not found"
        )
    return radusergroup


@router.put("/{id}", response_model=schemas.RadUserGroup)
async def update_radusergroup(
    *,
    db: AsyncSession = Depends(async_get_db),
    id: int,
    radusergroup_in: schemas.RadUserGroupUpdate
) -> Any:
    """Update a certain radusergroup assosication"""
    radusergroup = await crud.radusergroup.get(db=db, id=id)
    if not radusergroup:
        raise HTTPException(
            status_code=404, detail="RadUserGroup assosication not found"
        )
    radusergroup = await crud.radusergroup.update(
        db=db, db_obj=radusergroup, obj_in=radusergroup_in
    )
    return radusergroup


@router.delete("/{id}", response_model=schemas.RadUserGroup)
async def delete_radusergroup(
    *, db: AsyncSession = Depends(async_get_db), id: int
) -> Any:
    """Delete a radusergroup assosication"""
    radusergroup = await crud.radusergroup.get(db=db, id=id)
    if not radusergroup:
        raise HTTPException(
            status_code=404, detail="RadUserGroup assosication not found"
        )
    radusergroup = await crud.radusergroup.remove(db=db, id=id)
    return radusergroup
