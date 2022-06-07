from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import RadCheck, RadReply, RadUserGroup, RadAcct, RadPostAuth

from app.schemas.generic import AVPair
from app.schemas.user import (
    RadiusUser,
    RadiusUserCreate,
    RadiusUserUpdate,
    RadiusUserGroupAssosication,
)


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

    def get_by_username(self, db: Session, *, username: str) -> Optional[RadiusUser]:
        check_attributes = self.get_check_attributes(db=db, username=username)
        reply_attributes = self.get_reply_attributes(db=db, username=username)
        user_groups = self.get_user_groups(db=db, username=username)

        if not check_attributes and not reply_attributes and not user_groups:
            return None

        user = RadiusUser(
            username=username,
            groups=user_groups,
            check_attributes=check_attributes,
            reply_attributes=reply_attributes,
        )
        return user

    def remove_from_all_tables(
        self,
        db: Session,
        *,
        username: str,
        include_acct: bool = False,
        include_postauth: bool = False
    ) -> int:
        rows_deleted = 0

        rows_deleted += (
            db.query(RadCheck).filter(RadCheck.username == username).delete()
        )
        rows_deleted += (
            db.query(RadReply).filter(RadReply.username == username).delete()
        )
        rows_deleted += (
            db.query(RadUserGroup).filter(RadUserGroup.username == username).delete()
        )

        if include_acct:
            rows_deleted += (
                db.query(RadAcct).filter(RadAcct.username == username).delete()
            )

        if include_postauth:
            rows_deleted += (
                db.query(RadPostAuth).filter(RadPostAuth.username == username).delete()
            )
        db.commit()
        return rows_deleted


radiususer = CRUDRadiusUser(RadiusUser)
