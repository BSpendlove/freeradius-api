from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.radgroupcheck import RadGroupCheck
from app.schemas.radgroupcheck import RadGroupCheckCreate, RadGroupCheckUpdate


class CRUDRadGroupCheck(
    CRUDBase[RadGroupCheck, RadGroupCheckCreate, RadGroupCheckUpdate]
):
    def already_exist(
        self, db: Session, *, groupname: str, attribute: str, value: str
    ) -> bool:
        radgroupcheck = (
            db.query(RadGroupCheck)
            .filter(
                RadGroupCheck.groupname == groupname,
                RadGroupCheck.attribute == attribute,
                RadGroupCheck.value == value,
            )
            .first()
        )
        if not radgroupcheck:
            return False
        return True

    def create(self, db: Session, *, obj_in: RadGroupCheckCreate) -> RadGroupCheck:
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
        db_obj: RadGroupCheck,
        obj_in: Union[RadGroupCheckUpdate, Dict[str, Any]]
    ) -> RadGroupCheck:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)


radgroupcheck = CRUDRadGroupCheck(RadGroupCheck)
