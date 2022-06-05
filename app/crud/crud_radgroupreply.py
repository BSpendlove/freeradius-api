from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.radgroupreply import RadGroupReply
from app.schemas.radgroupreply import RadGroupReplyCreate, RadGroupReplyUpdate


class CRUDRadGroupReply(
    CRUDBase[RadGroupReply, RadGroupReplyCreate, RadGroupReplyUpdate]
):
    def already_exist(
        self, db: Session, *, groupname: str, attribute: str, value: str
    ) -> bool:
        radgroupreply = (
            db.query(RadGroupReply)
            .filter(
                RadGroupReply.groupname == groupname,
                RadGroupReply.attribute == attribute,
                RadGroupReply.value == value,
            )
            .first()
        )
        if not radgroupreply:
            return False
        return True

    def create(self, db: Session, *, obj_in: RadGroupReplyCreate) -> RadGroupReply:
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
        db_obj: RadGroupReply,
        obj_in: Union[RadGroupReplyUpdate, Dict[str, Any]]
    ) -> RadGroupReply:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)


radgroupreply = CRUDRadGroupReply(RadGroupReply)
