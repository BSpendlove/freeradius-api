from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.async_driver.base import CRUDBase
from app.models.radacct import RadAcct
from app.schemas.radacct import RadAcctCreate, RadAcctUpdate
from app.schemas.generic import GenericDeleteResponse
from app.config.app import settings


class CRUDRadAcct(CRUDBase[RadAcct, RadAcctCreate, RadAcctUpdate]):
    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[RadAcct]:
        if settings.PREFER_DATABASE_DESCENDING:
            results = await db.execute(
                select(self.model)
                .order_by(self.model.acctuniqueid.desc())
                .offset(skip)
                .limit(limit)
            )
        else:
            results = await db.execute(select(self.model).offset(skip).limit(limit))
        return results.scalars().all()

    async def get_multi_filter(
        self, db: AsyncSession, criterion: Tuple, skip: int = 0, limit: int = 100
    ) -> List[RadAcct]:
        if settings.PREFER_DATABASE_DESCENDING:
            results = await db.execute(
                select(self.model)
                .filter(*criterion)
                .order_by(self.model.acctuniqueid.desc())
                .offset(skip)
                .limit(limit)
            )
        else:
            results = await db.execute(
                select(self.model).filter(*criterion).offset(skip).limit(limit)
            )
        return results.scalars().all()

    async def get_by_username(
        self, db: AsyncSession, username: str, skip: int = 0, limit: int = 100
    ) -> Optional[List[RadAcct]]:
        results = await self.get_multi_filter(
            db=db, criterion=(self.model.username == username,), skip=skip, limit=limit
        )
        return results

    async def get_last_session_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[RadAcct]:
        results = await self.get_filter(
            db=db, criterion=(self.model.username == username,)
        )
        return results

    async def get_by_session_id(
        self, db: AsyncSession, session_id: str
    ) -> Optional[RadAcct]:
        results = await self.get_filter(
            db=db, criterion=(self.model.acctsessionid == session_id,)
        )
        return results

    async def remove_accounting_records(
        self, db: AsyncSession, username: str = ""
    ) -> GenericDeleteResponse:
        if not username:
            results = await self.remove_all(db=db)
        else:
            results = await self.remove_filter(
                db=db, criterion=(self.model.username == username,)
            )
        return {"rows_deleted": results}


radacct = CRUDRadAcct(RadAcct)
