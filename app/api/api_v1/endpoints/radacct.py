from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import require_api_key_auth, async_get_db
from app import schemas
import app.crud.async_driver as crud

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.get("/", response_model=List[schemas.RadAcct])
async def read_radacct_all(
    db: AsyncSession = Depends(async_get_db), skip: int = 0, limit=100
) -> Any:
    """Retrieve all radacct records"""
    radacct = await crud.radacct.get_multi(db=db, skip=skip, limit=limit)
    return radacct


@router.get("/{username}", response_model=List[schemas.RadAcct])
async def read_radacct_username(
    *,
    db: AsyncSession = Depends(async_get_db),
    username: str,
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Retrieve all radacct records for a specific username"""
    radacct = await crud.radacct.get_by_username(
        db=db, username=username, skip=skip, limit=limit
    )
    if not radacct:
        raise HTTPException(
            status_code=404, detail="No accounting records found for this Username"
        )
    return radacct


@router.get("/{username}", response_model=schemas.RadAcct)
async def read_radacct_username_latest(
    *, db: AsyncSession = Depends(async_get_db), username: str
) -> Any:
    """Retrieve the latest radacct record for a specific username"""
    radacct = await crud.radacct.get_last_AsyncSession_by_username(
        db=db, username=username
    )
    if not radacct:
        raise HTTPException(
            status_code=404, detail="No accounting records found for this Username"
        )
    return radacct


@router.delete("/", response_model=schemas.GenericDeleteResponse)
async def delete_radacct_all(*, db: AsyncSession = Depends(async_get_db)) -> Any:
    """Deletes all radacct records"""
    results = await crud.radacct.remove_accounting_records(db=db)
    return results


@router.delete("/{username}", response_model=schemas.GenericDeleteResponse)
async def delete_radacct_username(
    *, db: AsyncSession = Depends(async_get_db), username: str
) -> Any:
    """Deletes all radacct records for a specific username"""
    results = await crud.radacct.remove_accounting_records(db=db, username=username)
    return results
