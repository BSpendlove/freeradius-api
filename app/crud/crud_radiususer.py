from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.radcheck import RadCheck
from app.models.radreply import RadReply
from app.models.radusergroup import RadUserGroup

from app.schemas.generic import AVPair
from app.schemas.user import (
    RadiusUser,
    RadiusUserCreate,
    RadiusUserUpdate,
    RadiusUserGroupAssosication,
)

# from app.models.radusergroup import RadUserGroup
# from app.schemas.radusergroup import RadUserGroupCreate, RadUserGroupUpdate


class CRUDRadiusUser(CRUDBase[RadiusUser, RadiusUserCreate, RadiusUserUpdate]):
    def get_check_attributes(
        self, db: Session, *, username: str
    ) -> Optional[List[AVPair]]:
        attributes = db.query(RadCheck).filter(RadCheck.username == username).all()
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
        self, db: Session, *, username: str
    ) -> Optional[List[AVPair]]:
        attributes = db.query(RadReply).filter(RadReply.username == username).all()
        data = []
        for row in attributes:
            avpair = AVPair(
                id=row.id, attribute=row.attribute, op=row.op, value=row.value
            )
            data.append(avpair)
        return data

    def get_user_groups(
        self, db: Session, *, username: str
    ) -> Optional[List[RadiusUserGroupAssosication]]:
        groups = db.query(RadUserGroup).filter(RadUserGroup.username == username).all()
        data = []
        for row in groups:
            group = RadiusUserGroupAssosication(
                id=row.id, groupname=row.groupname, priority=row.priority
            )
            data.append(group)
        return data


radiususer = CRUDRadiusUser(RadiusUser)
