from typing import Any, Dict, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.nas import NAS
from app.schemas.nas import NASCreate, NASUpdate


class CRUDNAS(CRUDBase[NAS, NASCreate, NASUpdate]):
    def already_exist(self, db: Session, *, nasname: str, server: str) -> bool:
        nas = db.query(NAS).filter(NAS.nasname == nasname, NAS.server == server).first()
        if not nas:
            return False
        return True

    def create(self, db: Session, *, obj_in: NASCreate) -> NAS:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: NAS, obj_in: Union[NASUpdate, Dict[str, Any]]
    ) -> NAS:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)


nas = CRUDNAS(NAS)
