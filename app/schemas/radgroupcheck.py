from typing import Optional

from pydantic import BaseModel

from app.schemas.enums import OpEnum

# Shared properties
class RadGroupCheckBase(BaseModel):
    groupname: Optional[str]
    attribute: Optional[str]
    op: Optional[str]
    value: Optional[str]


# Properties to receive via API on creation
class RadGroupCheckCreate(RadGroupCheckBase):
    groupname: str
    attribute: str
    op: OpEnum
    value: str


# Properties to receive via API on update
class RadGroupCheckUpdate(BaseModel):
    value: str


class RadGroupCheckInDBBase(RadGroupCheckBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RadGroupCheckInDB(RadGroupCheckInDBBase):
    pass


class RadGroupCheck(RadGroupCheckInDB):
    pass
