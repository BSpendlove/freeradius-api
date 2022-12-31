from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import require_api_key_auth, async_get_db
from app import schemas
import app.crud.async_driver as crud

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.RadGroupReply)
async def create_radgroupreply(
    *,
    db: AsyncSession = Depends(async_get_db),
    radgroupreply_in: schemas.RadGroupReplyCreate
) -> Any:
    """Create a radgroupreply attribute"""
    radgroupreply = await crud.radgroupreply.already_exist(
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
    radgroupreply = await crud.radgroupreply.create(db=db, obj_in=radgroupreply_in)
    return radgroupreply


@router.get("/", response_model=List[schemas.RadGroupReply])
async def read_radgroupreply_all(
    db: AsyncSession = Depends(async_get_db), skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve all radgroupreply attributes"""
    radgroupreply = await crud.radgroupreply.get_multi(db=db, skip=skip, limit=limit)
    return radgroupreply


@router.get("/{id}", response_model=schemas.RadGroupReply)
async def read_radgroupreply(
    *, db: AsyncSession = Depends(async_get_db), id: int
) -> Any:
    """Retrieve a certain radgroupreply attribute"""
    radgroupreply = await crud.radgroupreply.get(db=db, id=id)
    if not radgroupreply:
        raise HTTPException(status_code=404, detail="RadGroupReply not found")
    return radgroupreply


@router.put("/{id}", response_model=schemas.RadGroupReply)
async def update_radgroupreply(
    *,
    db: AsyncSession = Depends(async_get_db),
    id: int,
    radgroupreply_in: schemas.RadGroupReplyUpdate
) -> Any:
    """Update a certain radgroupreply attribute"""
    radgroupreply = await crud.radgroupreply.get(db=db, id=id)
    if not radgroupreply:
        raise HTTPException(status_code=404, detail="RadGroupReply not found")
    radgroupreply = await crud.radgroupreply.update(
        db=db, db_obj=radgroupreply, obj_in=radgroupreply_in
    )
    return radgroupreply


@router.delete("/{id}", response_model=schemas.RadGroupReply)
async def delete_radgroupreply(
    *, db: AsyncSession = Depends(async_get_db), id: int
) -> Any:
    """Delete a radgroupreply attribute"""
    radgroupreply = await crud.radgroupreply.get(db=db, id=id)
    if not radgroupreply:
        raise HTTPException(status_code=404, detail="RadGroupReply not found")
    radgroupreply = await crud.radgroupreply.remove(db=db, id=id)
    return radgroupreply
