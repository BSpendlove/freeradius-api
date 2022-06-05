from typing import Optional

from pydantic import BaseModel

from app.schemas.enums import OpEnum

# Shared properties
class RadReplyBase(BaseModel):
    username: Optional[str]
    attribute: Optional[str]
    op: Optional[str]
    value: Optional[str]


# Properties to receive via API on creation
class RadReplyCreate(RadReplyBase):
    username: str
    attribute: str
    op: OpEnum
    value: str


# Properties to receive via API on update
class RadReplyUpdate(BaseModel):
    value: str


class RadReplyInDBBase(RadReplyBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RadReplyInDB(RadReplyInDBBase):
    pass


class RadReply(RadReplyInDB):
    pass
