from typing import Optional

from pydantic import BaseModel

# Shared properties
class RadUserGroupBase(BaseModel):
    username: Optional[str]
    groupname: Optional[str]
    priority: Optional[int]


# Properties to receive via API on creation
class RadUserGroupCreate(RadUserGroupBase):
    username: str
    groupname: str
    priority: int


# Properties to receive via API on update
class RadUserGroupUpdate(RadUserGroupBase):
    groupname: str


class RadUserGroupInDBBase(RadUserGroupBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RadUserGroupInDB(RadUserGroupInDBBase):
    pass


class RadUserGroup(RadUserGroupInDB):
    pass
