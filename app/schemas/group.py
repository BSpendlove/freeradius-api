from typing import Optional, List

from pydantic import BaseModel

from app.schemas.generic import AVPair


class RadiusGroupBase(BaseModel):
    groupname: Optional[str]


# Properties to receive via API on creation
class RadiusGroupCreate(RadiusGroupBase):
    groupname: str


# Properties to receive via API on update
class RadiusGroupUpdate(RadiusGroupBase):
    pass


class RadiusGroupUserAssosication(BaseModel):
    id: Optional[int] = None
    username: str
    priority: int


class RadiusGroup(RadiusGroupBase):
    users: Optional[List[RadiusGroupUserAssosication]]
    check_attributes: Optional[List[AVPair]]
    reply_attributes: Optional[List[AVPair]]
