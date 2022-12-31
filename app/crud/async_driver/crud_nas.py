from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.async_driver.base import CRUDBase
from app.models.nas import NAS
from app.schemas.nas import NASCreate, NASUpdate


class CRUDNAS(CRUDBase[NAS, NASCreate, NASUpdate]):
    async def already_exist(self, db: AsyncSession, nasname: str, server: str) -> bool:
        nas = await self.get_filter(
            db=db,
            criterion=(self.model.nasname == nasname, self.model.server == server),
        )
        if not nas:
            return False
        return True


nas = CRUDNAS(NAS)
