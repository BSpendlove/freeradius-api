from typing import Any, List
from ipaddress import IPv4Address

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_api_key, get_db
from app.config.app import settings
from app import crud, models, schemas
from app.modules.coa import COA

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.post("/{ip_address}", response_model=schemas.COAResponse)
def send_coa_request(ip_address: IPv4Address, coa_in: schemas.COABase) -> Any:
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


@router.post("/session/{session_id}", response_model=schemas.COAResponse)
def send_coa_request_using_session(
    *, db: Session = Depends(get_db), session_id: str, coa_in: schemas.COABase
) -> Any:
    """Send a COA request based on a specific accounting session ID in the database"""
    if not settings.VALIDATE_AVPAIRS:
        raise HTTPException(
            status_code=400,
            detail="VALIDATE_AVPAIRS must be True for this endpoint to be used",
        )

    if not coa_in.attributes:
        raise HTTPException(status_code=400, detail="No attributes provided")

    session = crud.radacct.get_by_session_id(db=db, session_id=session_id)
    if not session:
        raise HTTPException(
            status_code=404, detail="Unable to find session in the database"
        )

    ip_address = session.nasipaddress
    coa = COA(
        address=ip_address,
        secret=coa_in.secret,
        port=coa_in.port,
        timeout=coa_in.timeout,
        dictionary=settings.AVPAIRS_DICT,
    )

    response = coa.send_coa_packet(avpairs=coa_in.attributes)
    return response


@router.post("/session/username/{username}", response_model=schemas.COAResponse)
def send_coa_request_using_session(
    *, db: Session = Depends(get_db), username: str, coa_in: schemas.COABase
) -> Any:
    """Send a COA request based on the most recent session for a username in the database"""
    if not settings.VALIDATE_AVPAIRS:
        raise HTTPException(
            status_code=400,
            detail="VALIDATE_AVPAIRS must be True for this endpoint to be used",
        )

    if not coa_in.attributes:
        raise HTTPException(status_code=400, detail="No attributes provided")

    session = crud.radacct.get_last_session_by_username(db=db, username=username)
    if not session:
        raise HTTPException(
            status_code=404, detail="Unable to find session in the database"
        )

    ip_address = session.nasipaddress
    coa = COA(
        address=ip_address,
        secret=coa_in.secret,
        port=coa_in.port,
        timeout=coa_in.timeout,
        dictionary=settings.AVPAIRS_DICT,
    )

    response = coa.send_coa_packet(avpairs=coa_in.attributes)
    return response
