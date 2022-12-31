from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.async_driver.base import CRUDBase
from app.models.radusergroup import RadUserGroup
from app.schemas.radusergroup import RadUserGroupCreate, RadUserGroupUpdate


class CRUDRadUserGroup(CRUDBase[RadUserGroup, RadUserGroupCreate, RadUserGroupUpdate]):
    async def already_exist(
        self,
        db: AsyncSession,
        groupname: str,
        username: str,
    ) -> bool:
        results = await self.get_filter(
            db=db,
            criterion=(
                self.model.groupname == groupname,
                self.model.username == username,
            ),
        )
        if not results:
            return False
        return True


radusergroup = CRUDRadUserGroup(RadUserGroup)
