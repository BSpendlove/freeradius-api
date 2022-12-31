from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.async_driver.base import CRUDBase
from app.models.radgroupreply import RadGroupReply
from app.schemas.radgroupreply import RadGroupReplyCreate, RadGroupReplyUpdate


class CRUDRadGroupReply(
    CRUDBase[RadGroupReply, RadGroupReplyCreate, RadGroupReplyUpdate]
):
    async def already_exist(
        self, db: AsyncSession, groupname: str, attribute: str, value: str
    ) -> bool:
        results = await self.get_filter(
            db=db,
            criterion=(
                self.model.groupname == groupname,
                self.model.attribute == attribute,
                self.model.value == value,
            ),
        )
        if not results:
            return False
        return True

    async def already_exist_strict(
        self, db: AsyncSession, groupname: str, attribute: str, op: str, value: str
    ) -> bool:
        results = await self.get_filter(
            db=db,
            criterion=(
                self.model.groupname == groupname,
                self.model.attribute == attribute,
                self.model.op == op,
                self.model.value == value,
            ),
        )
        if not results:
            return False
        return True


radgroupreply = CRUDRadGroupReply(RadGroupReply)
