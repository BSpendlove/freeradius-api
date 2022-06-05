from typing import Optional, List

from pydantic import BaseModel

from app.schemas.generic import AVPair


class RadiusUserBase(BaseModel):
    username: Optional[str]


# Properties to receive via API on creation
class RadiusUserCreate(RadiusUserBase):
    username: str


# Properties to receive via API on update
class RadiusUserUpdate(RadiusUserBase):
    pass


class RadiusUserGroupAssosication(BaseModel):
    id: Optional[int] = None
    groupname: str
    priority: int


class RadiusUser(RadiusUserBase):
    groups: Optional[List[RadiusUserGroupAssosication]]
    check_attributes: Optional[List[AVPair]]
    reply_attributes: Optional[List[AVPair]]
