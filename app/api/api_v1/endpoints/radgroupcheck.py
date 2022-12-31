from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import require_api_key_auth, async_get_db
from app import schemas
import app.crud.async_driver as crud

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.RadGroupCheck)
async def create_radgroupcheck(
    *,
    db: AsyncSession = Depends(async_get_db),
    radgroupcheck_in: schemas.RadGroupCheckCreate
) -> Any:
    """Create a radgroupcheck attribute"""
    radgroupcheck = await crud.radgroupcheck.already_exist(
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
    radgroupcheck = await crud.radgroupcheck.create(db=db, obj_in=radgroupcheck_in)
    return radgroupcheck


@router.get("/", response_model=List[schemas.RadGroupCheck])
async def read_radgroupcheck_all(
    db: AsyncSession = Depends(async_get_db), skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve all radgroupcheck attributes"""
    radgroupcheck = await crud.radgroupcheck.get_multi(db=db, skip=skip, limit=limit)
    return radgroupcheck


@router.get("/{id}", response_model=schemas.RadGroupCheck)
async def read_radgroupcheck(
    *, db: AsyncSession = Depends(async_get_db), id: int
) -> Any:
    """Retrieve a certain radgroupcheck attribute"""
    radgroupcheck = await crud.radgroupcheck.get(db=db, id=id)
    if not radgroupcheck:
        raise HTTPException(status_code=404, detail="RadGroupCheck not found")
    return radgroupcheck


@router.put("/{id}", response_model=schemas.RadGroupCheck)
async def update_radgroupcheck(
    *,
    db: AsyncSession = Depends(async_get_db),
    id: int,
    radgroupcheck_in: schemas.RadGroupCheckUpdate
) -> Any:
    """Update a certain radgroupcheck attribute"""
    radgroupcheck = await crud.radgroupcheck.get(db=db, id=id)
    if not radgroupcheck:
        raise HTTPException(status_code=404, detail="RadGroupCheck not found")
    radgroupcheck = crud.radgroupcheck.update(
        db=db, db_obj=radgroupcheck, obj_in=radgroupcheck_in
    )
    return radgroupcheck


@router.delete("/{id}", response_model=schemas.RadGroupCheck)
async def delete_radgroupcheck(
    *, db: AsyncSession = Depends(async_get_db), id: int
) -> Any:
    """Delete a radgroupcheck attribute"""
    radgroupcheck = await crud.radgroupcheck.get(db=db, id=id)
    if not radgroupcheck:
        raise HTTPException(status_code=404, detail="RadGroupCheck not found")
    radgroupcheck = await crud.radgroupcheck.remove(db=db, id=id)
    return radgroupcheck
