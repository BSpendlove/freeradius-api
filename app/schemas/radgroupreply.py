from typing import Optional

from pydantic import BaseModel

from app.schemas.enums import OpEnum

# Shared properties
class RadGroupReplyBase(BaseModel):
    groupname: Optional[str]
    attribute: Optional[str]
    op: Optional[str]
    value: Optional[str]


# Properties to receive via API on creation
class RadGroupReplyCreate(RadGroupReplyBase):
    groupname: str
    attribute: str
    op: OpEnum
    value: str


# Properties to receive via API on update
class RadGroupReplyUpdate(BaseModel):
    value: str


class RadGroupReplyInDBBase(RadGroupReplyBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RadGroupReplyInDB(RadGroupReplyInDBBase):
    pass


class RadGroupReply(RadGroupReplyInDB):
    pass
