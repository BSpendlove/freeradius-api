from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.radacct import RadAcct
from app.schemas.radacct import RadAcctCreate, RadAcctUpdate
from app.schemas.generic import GenericDeleteResponse


class CRUDRadAcct(CRUDBase[RadAcct, RadAcctCreate, RadAcctUpdate]):
    def get_by_username(
        self, db: Session, *, username: str, skip: int = 0, limit: int = 100
    ) -> Optional[List[RadAcct]]:
        return self.get_multi_filter(
            db=db, criterion=(RadAcct.username == username), skip=skip, limit=limit
        )

    def remove_accounting_records(
        self, db: Session, *, username: str = ""
    ) -> GenericDeleteResponse:
        if not username:
            return {"rows_deleted": self.remove_all(db=db)}
        return {
            "rows_deleted": self.remove_filter(
                db=db, criterion=(RadAcct.username == username)
            )
        }


radacct = CRUDRadAcct(RadAcct)
