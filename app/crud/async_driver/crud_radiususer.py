from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.async_driver.base import CRUDBase
from app.models import RadCheck, RadReply, RadUserGroup, RadAcct, RadPostAuth
from app.schemas.generic import AVPair
from app.schemas.user import (
    RadiusUser,
    RadiusUserCreate,
    RadiusUserUpdate,
    RadiusUserGroupAssosication,
)
from app.crud.async_driver import radcheck


class CRUDRadiusUser(CRUDBase[RadiusUser, RadiusUserCreate, RadiusUserUpdate]):
    async def get_check_attributes(
        self, db: AsyncSession, *, username: str
    ) -> Optional[List[AVPair]]:
        attributes = await self.get_multi_filter_all_model(
            db=db, model=RadCheck, criterion=(RadCheck.username == username,)
        )
        data = []
        for attribute in attributes:
            avpair = AVPair(
                id=attribute.id,
                attribute=attribute.attribute,
                op=attribute.op,
                value=attribute.value,
            )
            data.append(avpair)
        return data

    async def get_reply_attributes(
        self, db: AsyncSession, username: str
    ) -> Optional[List[AVPair]]:
        attributes = await self.get_multi_filter_all_model(
            db=db, model=RadReply, criterion=(RadReply.username == username,)
        )
        data = []
        for attribute in attributes:
            avpair = AVPair(
                id=attribute.id,
                attribute=attribute.attribute,
                op=attribute.op,
                value=attribute.value,
            )
            data.append(avpair)
        return data

    async def get_user_groups(
        self, db: AsyncSession, username: str
    ) -> Optional[List[RadiusUserGroupAssosication]]:
        groups = await self.get_multi_filter_all_model(
            db=db, model=RadUserGroup, criterion=(RadUserGroup.username == username,)
        )
        data = []
        for row in groups:
            group = RadiusUserGroupAssosication(
                id=row.id, groupname=row.groupname, priority=row.priority
            )
            data.append(group)
        return data

    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[RadiusUser]:
        check_attributes = await self.get_check_attributes(db=db, username=username)
        reply_attributes = await self.get_reply_attributes(db=db, username=username)
        user_groups = await self.get_user_groups(db=db, username=username)

        if not check_attributes and not reply_attributes and not user_groups:
            return None

        user = RadiusUser(
            username=username,
            groups=user_groups,
            check_attributes=check_attributes,
            reply_attributes=reply_attributes,
        )
        return user

    async def remove_from_all_tables(
        self,
        db: AsyncSession,
        username: str,
        include_acct: bool = False,
        include_postauth: bool = False,
    ) -> int:
        rows_deleted = 0

        rows_deleted = await self.remove_filter_model(
            db=db, model=RadCheck, criterion=(RadCheck.username == username,)
        )
        rows_deleted = await self.remove_filter_model(
            db=db, model=RadReply, criterion=(RadReply.username == username,)
        )
        rows_deleted = await self.remove_filter_model(
            db=db, model=RadUserGroup, criterion=(RadUserGroup.username == username,)
        )

        if include_acct:
            rows_deleted = await self.remove_filter_model(
                db=db, model=RadAcct, criterion=(RadAcct.username == username)
            )

        if include_postauth:
            rows_deleted = await self.remove_filter_model(
                db=db, model=RadPostAuth, criterion=(RadPostAuth.username == username)
            )

        return rows_deleted


radiususer = CRUDRadiusUser(RadiusUser)
