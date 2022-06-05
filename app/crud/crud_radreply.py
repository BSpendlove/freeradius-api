from typing import Any, Dict, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.radreply import RadReply
from app.schemas.radreply import RadReplyCreate, RadReplyUpdate


class CRUDRadReply(CRUDBase[RadReply, RadReplyCreate, RadReplyUpdate]):
    def already_exist(
        self, db: Session, *, username: str, attribute: str, value: str
    ) -> bool:
        radreply = (
            db.query(RadReply)
            .filter(
                RadReply.username == username,
                RadReply.attribute == attribute,
                RadReply.value == value,
            )
            .first()
        )
        if not radreply:
            return False
        return True

    def create(self, db: Session, *, obj_in: RadReplyCreate) -> RadReply:
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
        db_obj: RadReply,
        obj_in: Union[RadReplyUpdate, Dict[str, Any]]
    ) -> RadReply:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)


radreply = CRUDRadReply(RadReply)
