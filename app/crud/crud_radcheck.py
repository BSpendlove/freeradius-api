from typing import Any, Dict, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.radcheck import RadCheck
from app.schemas.radcheck import RadCheckCreate, RadCheckUpdate


class CRUDRadCheck(CRUDBase[RadCheck, RadCheckCreate, RadCheckUpdate]):
    def already_exist(
        self, db: Session, *, username: str, attribute: str, value: str
    ) -> bool:
        radcheck = (
            db.query(RadCheck)
            .filter(
                RadCheck.username == username,
                RadCheck.attribute == attribute,
                RadCheck.value == value,
            )
            .first()
        )
        if not radcheck:
            return False
        return True

    def create(self, db: Session, *, obj_in: RadCheckCreate) -> RadCheck:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: RadCheck,
        obj_in: Union[RadCheckUpdate, Dict[str, Any]]
    ) -> RadCheck:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)


radcheck = CRUDRadCheck(RadCheck)
