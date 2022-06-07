from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import RadGroupCheck, RadGroupReply, RadUserGroup, RadAcct, RadPostAuth

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

    def get_by_groupname(self, db: Session, *, groupname: str) -> RadiusGroup:
        check_attributes = self.get_check_attributes(db=db, groupname=groupname)
        reply_attributes = self.get_reply_attributes(db=db, groupname=groupname)
        users = self.get_users(db=db, groupname=groupname)

        if not check_attributes and not reply_attributes and not users:
            return None

        group = RadiusGroup(
            groupname=groupname,
            users=users,
            check_attributes=check_attributes,
            reply_attributes=reply_attributes,
        )
        return group

    def remove_from_all_tables(self, db: Session, *, groupname: str) -> int:
        rows_deleted = 0

        rows_deleted += (
            db.query(RadGroupCheck)
            .filter(RadGroupCheck.groupname == groupname)
            .delete()
        )
        rows_deleted += (
            db.query(RadGroupReply)
            .filter(RadGroupReply.groupname == groupname)
            .delete()
        )
        rows_deleted += (
            db.query(RadUserGroup).filter(RadUserGroup.groupname == groupname).delete()
        )

        db.commit()
        return rows_deleted


radiusgroup = CRUDRadiusGroup(RadiusGroup)
