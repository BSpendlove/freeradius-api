from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.async_driver.base import CRUDBase
from app.models import RadGroupCheck, RadGroupReply, RadUserGroup, RadAcct, RadPostAuth
from app.schemas.generic import AVPair
from app.schemas.group import (
    RadiusGroup,
    RadiusGroupCreate,
    RadiusGroupUpdate,
    RadiusGroupUserAssosication,
)


class CRUDRadiusGroup(CRUDBase[RadiusGroup, RadiusGroupCreate, RadiusGroupUpdate]):
    async def get_check_attributes(
        self, db: AsyncSession, groupname: str
    ) -> Optional[List[AVPair]]:
        attributes = await self.get_multi_filter_all_model(
            db=db,
            model=RadGroupCheck,
            criterion=(RadGroupCheck.groupname == groupname,),
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
        self, db: AsyncSession, groupname: str
    ) -> Optional[List[AVPair]]:
        attributes = await self.get_multi_filter_all_model(
            db=db,
            model=RadGroupReply,
            criterion=(RadGroupReply.groupname == groupname,),
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

    async def get_users(
        self, db: AsyncSession, groupname: str
    ) -> Optional[List[RadiusGroupUserAssosication]]:
        group_users = await self.get_multi_filter_all_model(
            db=db, model=RadUserGroup, criterion=(RadUserGroup.groupname == groupname,)
        )
        data = []
        for user in group_users:
            user = RadiusGroupUserAssosication(
                id=user.id, username=user.username, priority=user.priority
            )
            data.append(user)
        return data

    async def get_by_groupname(self, db: AsyncSession, groupname: str) -> RadiusGroup:
        check_attributes = await self.get_check_attributes(db=db, groupname=groupname)
        reply_attributes = await self.get_reply_attributes(db=db, groupname=groupname)
        users = await self.get_users(db=db, groupname=groupname)

        if not check_attributes and not reply_attributes and not users:
            return None

        group = RadiusGroup(
            groupname=groupname,
            users=users,
            check_attributes=check_attributes,
            reply_attributes=reply_attributes,
        )
        return group

    def remove_from_all_tables(self, db: AsyncSession, groupname: str) -> int:
        rows_deleted = 0
        rows_deleted += self.remove_filter_model(
            db=db,
            model=RadGroupCheck,
            criterion=(RadGroupCheck.groupname == groupname,),
        )
        rows_deleted += self.remove_filter_model(
            db=db,
            model=RadGroupReply,
            criterion=(RadGroupReply.groupname == groupname,),
        )
        rows_deleted += self.remove_filter_model(
            db=db, model=RadUserGroup, criterion=(RadUserGroup.groupname == groupname,)
        )
        return rows_deleted


radiusgroup = CRUDRadiusGroup(RadiusGroup)
