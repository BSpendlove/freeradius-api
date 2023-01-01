from typing import Any, List
from ipaddress import IPv4Address
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import require_api_key_auth, async_get_db
from app.config.app import settings
from app import schemas
from app.modules.coa import COA
import app.crud.async_driver as crud

router = APIRouter(dependencies=[Depends(require_api_key_auth)])


@router.post("/{ip_address}", response_model=schemas.COAResponse)
async def send_coa_request(ip_address: IPv4Address, coa_in: schemas.COABase) -> Any:
    """Generate a COA request and send to the device"""
    if not settings.VALIDATE_AVPAIRS:
        raise HTTPException(
            status_code=400,
            detail="VALIDATE_AVPAIRS must be True for this endpoint to be used",
        )

    if not coa_in.attributes:
        raise HTTPException(status_code=400, detail="No attributes provided")

    ip_address_str = str(ip_address)

    coa = COA(
        address=ip_address_str,
        secret=coa_in.secret,
        port=coa_in.port,
        timeout=coa_in.timeout,
        dictionary=settings.AVPAIRS_DICT,
    )

    response = coa.send_coa_packet(avpairs=coa_in.attributes)
    return response


@router.post("/AsyncSession/{AsyncSession_id}", response_model=schemas.COAResponse)
async def send_coa_request_using_AsyncSession(
    *,
    db: AsyncSession = Depends(async_get_db),
    AsyncSession_id: str,
    coa_in: schemas.COABase
) -> Any:
    """Send a COA request based on a specific accounting AsyncSession ID in the database"""
    if not settings.VALIDATE_AVPAIRS:
        raise HTTPException(
            status_code=400,
            detail="VALIDATE_AVPAIRS must be True for this endpoint to be used",
        )

    if not coa_in.attributes:
        raise HTTPException(status_code=400, detail="No attributes provided")

    AsyncSession = await crud.radacct.get_by_AsyncSession_id(
        db=db, AsyncSession_id=AsyncSession_id
    )
    if not AsyncSession:
        raise HTTPException(
            status_code=404, detail="Unable to find AsyncSession in the database"
        )

    ip_address = AsyncSession.nasipaddress
    coa = COA(
        address=ip_address,
        secret=coa_in.secret,
        port=coa_in.port,
        timeout=coa_in.timeout,
        dictionary=settings.AVPAIRS_DICT,
    )

    response = coa.send_coa_packet(avpairs=coa_in.attributes)
    return response


@router.post("/AsyncSession/username/{username}", response_model=schemas.COAResponse)
async def send_coa_request_using_AsyncSession(
    *, db: AsyncSession = Depends(async_get_db), username: str, coa_in: schemas.COABase
) -> Any:
    """Send a COA request based on the most recent AsyncSession for a username in the database"""
    if not settings.VALIDATE_AVPAIRS:
        raise HTTPException(
            status_code=400,
            detail="VALIDATE_AVPAIRS must be True for this endpoint to be used",
        )

    if not coa_in.attributes:
        raise HTTPException(status_code=400, detail="No attributes provided")

    AsyncSession = await crud.radacct.get_last_AsyncSession_by_username(
        db=db, username=username
    )
    if not AsyncSession:
        raise HTTPException(
            status_code=404, detail="Unable to find AsyncSession in the database"
        )

    ip_address = AsyncSession.nasipaddress
    coa = COA(
        address=ip_address,
        secret=coa_in.secret,
        port=coa_in.port,
        timeout=coa_in.timeout,
        dictionary=settings.AVPAIRS_DICT,
    )

    response = coa.send_coa_packet(avpairs=coa_in.attributes)
    return response
