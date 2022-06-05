from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class RadAcctBase(BaseModel):
    radacctid: Optional[int]
    acctsessionid: Optional[str]
    acctuniqueid: Optional[str]
    username: Optional[str]
    realm: Optional[str]
    nasipaddress: Optional[str]
    nasportid: Optional[str]
    nasporttype: Optional[str]
    acctstarttime: Optional[datetime]
    acctupdatetime: Optional[datetime]
    acctstoptime: Optional[datetime]
    acctinterval: Optional[int]
    acctsessiontime: Optional[int]
    acctauthentic: Optional[str]
    connectinfo_start: Optional[str]
    connectinfo_stop: Optional[str]
    acctinputoctets: Optional[int]
    acctoutputoctets: Optional[int]
    calledstationid: Optional[str]
    callingstationid: Optional[str]
    acctterminatecause: Optional[str]
    servicetype: Optional[str]
    framedprotocol: Optional[str]
    framedipaddress: Optional[str]
    framedipv6address: Optional[str]
    framedipv6prefix: Optional[str]
    framedinterfaceid: Optional[str]
    delegatedipv6prefix: Optional[str]


# Properties to receive via API on creation
# NOT IMPLEMENTED - FreeRADIUS should INSERT records into the database directly
class RadAcctCreate(RadAcctBase):
    pass


# Properties to receive via API on update
# NOT IMPLEMENTED - FreeRADIUS should INSERT records into the database directly
class RadAcctUpdate(RadAcctBase):
    pass


class RadAcctInDBBase(RadAcctBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RadAcctInDB(RadAcctInDBBase):
    pass


class RadAcct(RadAcctInDB):
    pass
