from typing import Optional

from pydantic import BaseModel

# Shared properties
class NASBase(BaseModel):
    nasname: Optional[str]
    shortname: Optional[str]
    type: Optional[str]
    ports: Optional[int]
    secret: Optional[str]
    server: Optional[str]
    community: Optional[str]
    description: Optional[str]


# Properties to receive via API on creation
class NASCreate(NASBase):
    nasname: str
    community: str


# Properties to receive via API on update
class NASUpdate(NASBase):
    nasname: str


class NASInDBBase(NASBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class NASInDB(NASInDBBase):
    pass


class NAS(NASInDB):
    pass
