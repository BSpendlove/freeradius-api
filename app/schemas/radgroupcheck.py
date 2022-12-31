from typing import Optional

from pydantic import BaseModel

from app.schemas.enums import OpEnum

# Shared properties
class RadGroupCheckBase(BaseModel):
    groupname: str
    attribute: str
    op: str
    value: str


# Properties to receive via API on creation
class RadGroupCheckCreate(RadGroupCheckBase):
    pass


# Properties to receive via API on update
class RadGroupCheckUpdate(BaseModel):
    pass


class RadGroupCheckInDBBase(RadGroupCheckBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RadGroupCheckInDB(RadGroupCheckInDBBase):
    pass


class RadGroupCheck(RadGroupCheckInDB):
    pass
