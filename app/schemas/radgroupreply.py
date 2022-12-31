from typing import Optional

from pydantic import BaseModel

from app.schemas.enums import OpEnum

# Shared properties
class RadGroupReplyBase(BaseModel):
    groupname: str
    attribute: str
    op: str
    value: str


# Properties to receive via API on creation
class RadGroupReplyCreate(RadGroupReplyBase):
    pass


# Properties to receive via API on update
class RadGroupReplyUpdate(BaseModel):
    pass


class RadGroupReplyInDBBase(RadGroupReplyBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RadGroupReplyInDB(RadGroupReplyInDBBase):
    pass


class RadGroupReply(RadGroupReplyInDB):
    pass
