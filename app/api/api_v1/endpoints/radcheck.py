from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import require_api_key_auth, async_get_db
from app import schemas
import app.crud.async_driver as crud

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/", response_model=schemas.RadCheck)
async def create_radcheck(
    *, db: AsyncSession = Depends(async_get_db), radcheck_in: schemas.RadCheckCreate
) -> Any:
    """Create a radcheck attribute"""
    radcheck = await crud.radcheck.already_exist(
        db=db,
        username=radcheck_in.username,
        attribute=radcheck_in.attribute,
        value=radcheck_in.value,
    )
    if radcheck:
        raise HTTPException(
            status_code=400,
            detail="Username with these attributes already exist (op value not compared)",
        )

    radcheck = await crud.radcheck.create(db=db, obj_in=radcheck_in)
    return radcheck


@router.get("/", response_model=List[schemas.RadCheck])
async def read_radcheck_all(
    db: AsyncSession = Depends(async_get_db), skip: int = 0, limit=100
) -> Any:
    """Retrieve all radcheck attributes"""
    radcheck = await crud.radcheck.get_multi(db=db, skip=skip, limit=limit)
    return radcheck


@router.get("/{id}", response_model=schemas.RadCheck)
async def read_radcheck(*, db: AsyncSession = Depends(async_get_db), id: int) -> Any:
    """Retrieve a certain radcheck attribute"""
    radcheck = await crud.radcheck.get(db=db, id=id)
    if not radcheck:
        raise HTTPException(status_code=404, detail="RadCheck not found")
    return radcheck


@router.put("/{id}", response_model=schemas.RadCheck)
async def update_radcheck(
    *,
    db: AsyncSession = Depends(async_get_db),
    id: int,
    radcheck_in: schemas.RadCheckUpdate
) -> Any:
    """Update a certain radcheck attribute"""
    radcheck = await crud.radcheck.get(db=db, id=id)
    if not radcheck:
        raise HTTPException(status_code=404, detail="RadCheck not found")
    radcheck = await crud.radcheck.update(db=db, db_obj=radcheck, obj_in=radcheck_in)
    return radcheck


@router.delete("/{id}", response_model=schemas.RadCheck)
async def delete_radcheck(*, db: AsyncSession = Depends(async_get_db), id: int) -> Any:
    """Delete a radcheck attribute"""
    radcheck = await crud.radcheck.get(db=db, id=id)
    if not radcheck:
        raise HTTPException(status_code=404, detail="RadCheck not found")
    radcheck = await crud.radcheck.remove(db=db, id=id)
    return radcheck
