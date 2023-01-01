from typing import Optional

from pydantic import BaseModel

from app.schemas.enums import OpEnum

# Shared properties
class RadReplyBase(BaseModel):
    username: str
    attribute: str
    op: str
    value: str


# Properties to receive via API on creation
class RadReplyCreate(RadReplyBase):
    pass


# Properties to receive via API on update
class RadReplyUpdate(BaseModel):
    pass


class RadReplyInDBBase(RadReplyBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RadReplyInDB(RadReplyInDBBase):
    pass


class RadReply(RadReplyInDB):
    pass
