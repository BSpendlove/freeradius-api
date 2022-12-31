from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import require_api_key_auth, async_get_db
from app import schemas
import app.crud.async_driver as crud

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.RadReply)
async def create_radreply(
    *, db: AsyncSession = Depends(async_get_db), radreply_in: schemas.RadReplyCreate
) -> Any:
    """Create a radreply attribute"""
    radreply = await crud.radreply.already_exist(
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

    radreply = await crud.radreply.create(db=db, obj_in=radreply_in)
    return radreply


@router.get("/", response_model=List[schemas.RadReply])
async def read_radreply_all(
    db: AsyncSession = Depends(async_get_db), skip: int = 0, limit=100
) -> Any:
    """Retrieve all radreply attributes."""
    radreply = await crud.radreply.get_multi(db=db, skip=skip, limit=limit)
    return radreply


@router.get("/{id}", response_model=schemas.RadReply)
async def read_radreply(*, db: AsyncSession = Depends(async_get_db), id: int) -> Any:
    """Retrieve a certain radreply attribute"""
    radreply = await crud.radreply.get(db=db, id=id)
    if not radreply:
        raise HTTPException(status_code=404, detail="RadReply not found")
    return radreply


@router.put("/{id}", response_model=schemas.RadReply)
async def update_radreply(
    *,
    db: AsyncSession = Depends(async_get_db),
    id: int,
    radreply_in: schemas.RadReplyUpdate
) -> Any:
    """Update a certain radreply attribute"""
    radreply = await crud.radreply.get(db=db, id=id)
    if not radreply:
        raise HTTPException(status_code=404, detail="RadReply not found")
    radreply = await crud.radreply.update(db=db, db_obj=radreply, obj_in=radreply_in)
    return radreply


@router.delete("/{id}", response_model=schemas.RadReply)
async def delete_radreply(*, db: AsyncSession = Depends(async_get_db), id: int) -> Any:
    """Delete a radreply attribute"""
    radreply = await crud.radreply.get(db=db, id=id)
    if not radreply:
        raise HTTPException(status_code=404, detail="RadReply not found")
    radreply = await crud.radreply.remove(db=db, id=id)
    return radreply
