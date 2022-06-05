from typing import Any, Dict, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.radusergroup import RadUserGroup
from app.schemas.radusergroup import RadUserGroupCreate, RadUserGroupUpdate


class CRUDRadUserGroup(CRUDBase[RadUserGroup, RadUserGroupCreate, RadUserGroupUpdate]):
    def already_exist(
        self,
        db: Session,
        *,
        groupname: str,
        username: str,
    ) -> bool:
        radusergroup = (
            db.query(RadUserGroup)
            .filter(
                RadUserGroup.groupname == groupname, RadUserGroup.username == username
            )
            .first()
        )
        if not radusergroup:
            return False
        return True

    def create(self, db: Session, *, obj_in: RadUserGroupCreate) -> RadUserGroup:
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
        db_obj: RadUserGroup,
        obj_in: Union[RadUserGroupUpdate, Dict[str, Any]],
    ) -> RadUserGroup:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)


radusergroup = CRUDRadUserGroup(RadUserGroup)
