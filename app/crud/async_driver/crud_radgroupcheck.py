from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.async_driver.base import CRUDBase
from app.models.radgroupcheck import RadGroupCheck
from app.schemas.radgroupcheck import RadGroupCheckCreate, RadGroupCheckUpdate


class CRUDRadGroupCheck(
    CRUDBase[RadGroupCheck, RadGroupCheckCreate, RadGroupCheckUpdate]
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


radgroupcheck = CRUDRadGroupCheck(RadGroupCheck)
