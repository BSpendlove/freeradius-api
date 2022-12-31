from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.async_driver.base import CRUDBase
from app.models.radreply import RadReply
from app.schemas.radreply import RadReplyCreate, RadReplyUpdate


class CRUDRadReply(CRUDBase[RadReply, RadReplyCreate, RadReplyUpdate]):
    async def already_exist(
        self, db: AsyncSession, username: str, attribute: str, value: str
    ) -> bool:
        results = await self.get_filter(
            db=db,
            criterion=(
                self.model.username == username,
                self.model.attribute == attribute,
                self.model.value == value,
            ),
        )
        if not results:
            return False
        return True

    async def already_exist_attribute(
        self, db: AsyncSession, username: str, attribute: str
    ) -> bool:
        results = await self.get_filter(
            db=db,
            criterion=(
                self.model.username == username,
                self.model.attribute == attribute,
            ),
        )
        if not results:
            return False
        return True


radreply = CRUDRadReply(RadReply)
