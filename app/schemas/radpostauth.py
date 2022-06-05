from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class RadPostAuthBase(BaseModel):
    username: Optional[str]
    _pass: Optional[str]
    reply: Optional[str]
    authdate: Optional[datetime]

    class Config:
        fields = {"_pass": "pass"}


# Properties to receive via API on creation
# NOT IMPLEMENTED - FreeRADIUS should INSERT records into the database directly
class RadPostAuthCreate(RadPostAuthBase):
    pass


# Properties to receive via API on update
# NOT IMPLEMENTED - FreeRADIUS should INSERT records into the database directly
class RadPostAuthUpdate(RadPostAuthBase):
    pass


class RadPostAuthInDBBase(RadPostAuthBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RadPostAuthInDB(RadPostAuthInDBBase):
    pass


class RadPostAuth(RadPostAuthInDB):
    pass
