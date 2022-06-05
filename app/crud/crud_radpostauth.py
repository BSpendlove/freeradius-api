from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.radpostauth import RadPostAuth
from app.schemas.radpostauth import RadPostAuthCreate, RadPostAuthUpdate
from app.schemas.generic import GenericDeleteResponse


class CRUDRadPostAuth(CRUDBase[RadPostAuth, RadPostAuthCreate, RadPostAuthUpdate]):
    def get_by_username(
        self, db: Session, *, username: str, skip: int = 0, limit: int = 100
    ) -> Optional[List[RadPostAuth]]:
        return self.get_multi_filter(
            db=db, criterion=(RadPostAuth.username == username), skip=skip, limit=limit
        )

    def remove_postauth_records(
        self, db: Session, *, username: str = ""
    ) -> GenericDeleteResponse:
        if not username:
            return {"rows_deleted": self.remove_all(db=db)}

        return {
            "rows_deleted": self.remove_filter(
                db=db, criterion=(RadPostAuth.username == username)
            )
        }


radpostauth = CRUDRadPostAuth(RadPostAuth)
