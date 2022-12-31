from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import require_api_key_auth, async_get_db
from app import schemas
import app.crud.async_driver as crud

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.get("/", response_model=List[schemas.RadPostAuth])
async def read_radpostauth_all(
    db: AsyncSession = Depends(async_get_db), skip: int = 0, limit=100
) -> Any:
    """Retrieve all radpostauth records"""
    radpostauth = await crud.radpostauth.get_multi(db=db, skip=skip, limit=limit)
    return radpostauth


@router.get("/{username}", response_model=List[schemas.RadPostAuth])
async def read_radpostauth_username(
    *,
    db: AsyncSession = Depends(async_get_db),
    username: str,
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Retrieve all radpostauth records for a specific username"""
    radpostauth = await crud.radpostauth.get_by_username(
        db=db, username=username, skip=skip, limit=limit
    )
    if not radpostauth:
        raise HTTPException(
            status_code=404, detail="No postauth records found for this Username"
        )
    return radpostauth


@router.delete("/", response_model=schemas.GenericDeleteResponse)
async def delete_radpostauth_all(*, db: AsyncSession = Depends(async_get_db)) -> Any:
    """Deletes all radpostauth records"""
    return await crud.radpostauth.remove_all(db=db)


@router.delete("/{username}", response_model=schemas.GenericDeleteResponse)
async def delete_radpostauth_username(
    *, db: AsyncSession = Depends(async_get_db), username: str
) -> Any:
    """Deletes all radpostauth records for a specific username"""
    return await crud.radpostauth.remove_postauth_records(db=db, username=username)
