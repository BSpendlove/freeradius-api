from typing import Optional, List

from pydantic import BaseModel

from app.schemas.generic import AVPair


class RadiusGroupBase(BaseModel):
    groupname: Optional[str]


class RadiusGroupUserAssosication(BaseModel):
    id: Optional[int] = None
    username: str
    priority: int


class RadiusGroup(RadiusGroupBase):
    users: Optional[List[RadiusGroupUserAssosication]] = []
    check_attributes: Optional[List[AVPair]] = []
    reply_attributes: Optional[List[AVPair]] = []


# Properties to receive via API on creation
class RadiusGroupCreate(RadiusGroup):
    groupname: str


# Properties to receive via API on update
class RadiusGroupUpdate(RadiusGroup):
    pass
