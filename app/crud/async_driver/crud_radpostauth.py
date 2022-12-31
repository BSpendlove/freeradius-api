from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.async_driver.base import CRUDBase
from app.models.radpostauth import RadPostAuth
from app.schemas.radpostauth import RadPostAuthCreate, RadPostAuthUpdate
from app.schemas.generic import GenericDeleteResponse


class CRUDRadPostAuth(CRUDBase[RadPostAuth, RadPostAuthCreate, RadPostAuthUpdate]):
    async def get_by_username(
        self, db: AsyncSession, username: str, skip: int = 0, limit: int = 100
    ) -> Optional[List[RadPostAuth]]:
        results = await self.get_multi_filter(
            db=db, criterion=(self.model.username == username,), skip=skip, limit=limit
        )
        return results

    async def remove_postauth_records(
        self, db: AsyncSession, username: str = ""
    ) -> GenericDeleteResponse:
        if not username:
            results = await self.remove_all(db=db)
        else:
            results = await self.remove_filter(
                db=db, criterion=(self.model.username == username,)
            )

        return {"rows_deleted": results}


radpostauth = CRUDRadPostAuth(RadPostAuth)
