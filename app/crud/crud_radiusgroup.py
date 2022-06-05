from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.radgroupcheck import RadGroupCheck
from app.models.radgroupreply import RadGroupReply
from app.models.radusergroup import RadUserGroup

from app.schemas.generic import AVPair
from app.schemas.group import (
    RadiusGroup,
    RadiusGroupCreate,
    RadiusGroupUpdate,
    RadiusGroupUserAssosication,
)


class CRUDRadiusGroup(CRUDBase[RadiusGroup, RadiusGroupCreate, RadiusGroupUpdate]):
    def get_check_attributes(
        self, db: Session, *, groupname: str
    ) -> Optional[List[AVPair]]:
        attributes = (
            db.query(RadGroupCheck).filter(RadGroupCheck.groupname == groupname).all()
        )
        data = []
        for row in attributes:
            avpair = AVPair(
                id=row.id,
                attribute=row.attribute,
                op=row.op,
                value=row.value,
            )
            data.append(avpair)
        return data

    def get_reply_attributes(
        self, db: Session, *, groupname: str
    ) -> Optional[List[AVPair]]:
        attributes = (
            db.query(RadGroupReply).filter(RadGroupReply.groupname == groupname).all()
        )
        data = []
        for row in attributes:
            avpair = AVPair(
                id=row.id, attribute=row.attribute, op=row.op, value=row.value
            )
            data.append(avpair)
        return data

    def get_users(
        self, db: Session, *, groupname: str
    ) -> Optional[List[RadiusGroupUserAssosication]]:
        group_users = (
            db.query(RadUserGroup).filter(RadUserGroup.groupname == groupname).all()
        )
        data = []
        for row in group_users:
            user = RadiusGroupUserAssosication(
                id=row.id, username=row.username, priority=row.priority
            )
            data.append(user)
        return data


radiusgroup = CRUDRadiusGroup(RadiusGroup)
