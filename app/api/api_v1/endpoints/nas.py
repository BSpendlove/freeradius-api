from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import require_api_key_auth, async_get_db
from app import schemas
import app.crud.async_driver as crud

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.NAS)
async def create_nas(
    *, db: AsyncSession = Depends(async_get_db), nas_in: schemas.NASCreate
) -> Any:
    """Create a NAS client"""
    nas = await crud.nas.already_exist(
        db=db, nasname=nas_in.nasname, server=nas_in.server
    )
    if nas:
        raise HTTPException(
            status_code=400, detail="NAS client with these attributes already exist"
        )
    nas = await crud.nas.create(db=db, obj_in=nas_in)
    return nas


@router.get("/", response_model=List[schemas.NAS])
async def read_nas_all(
    db: AsyncSession = Depends(async_get_db), skip: int = 0, limit: int = 100
) -> Any:
    """Retrieve all NAS clients"""
    nas = await crud.nas.get_multi(db=db, skip=skip, limit=limit)
    return nas


@router.get("/{id}", response_model=schemas.NAS)
async def rad_nas(*, db: AsyncSession = Depends(async_get_db), id: int) -> Any:
    """Retrieve a certain NAS client"""
    nas = await crud.nas.get(db=db, id=id)
    if not nas:
        raise HTTPException(status_code=404, detail="NAS client not found")
    return nas


@router.put("/{id}", response_model=schemas.NAS)
async def update_nas(
    *, db: AsyncSession = Depends(async_get_db), id: int, nas_in: schemas.NASUpdate
) -> Any:
    """Update a certain NAS client"""
    nas = await crud.nas.get(db=db, id=id)
    if not nas:
        raise HTTPException(status_code=404, detail="NAS client not found")
    nas = await crud.nas.update(db=db, db_obj=nas, obj_in=nas_in)
    return nas


@router.delete("/{id}", response_model=schemas.NAS)
async def delete_nas(*, db: AsyncSession = Depends(async_get_db), id: int) -> Any:
    """Delete a NAS client"""
    nas = await crud.nas.get(db=db, id=id)
    if not nas:
        raise HTTPException(status_code=404, detail="NAS client not found")
    nas = await crud.nas.remove(db=db, id=id)
    return nas
