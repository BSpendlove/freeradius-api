from typing import Optional

from pydantic import BaseModel

from app.schemas.enums import OpEnum

# Shared properties
class RadCheckBase(BaseModel):
    username: str
    attribute: str
    op: str
    value: str


# Properties to receive via API on creation
class RadCheckCreate(RadCheckBase):
    pass


# Properties to receive via API on update
class RadCheckUpdate(RadCheckBase):
    value: str


class RadCheckInDBBase(RadCheckBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RadCheckInDB(RadCheckInDBBase):
    pass


class RadCheck(RadCheckInDB):
    pass
