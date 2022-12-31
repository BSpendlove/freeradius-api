from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import Base
from app.config.app import settings

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """CRUD Object with default methods to Create, Read, Update and Delete (CRUD).

        Arguments:
            model:  A SQLAlchemy model class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        results = await db.execute(select(self.model).filter(self.model.id == id))
        return results.scalars().first()

    async def get_filter(self, db: AsyncSession, criterion: Tuple) -> ModelType:
        results = await db.execute(select(self.model).filter(*criterion))
        return results.scalars().first()

    async def get_filter_like(
        self, db: AsyncSession, criterion: Tuple, column, expr: str
    ) -> ModelType:
        query = select(self.model).filter(*criterion).where(column.ilike(expr))
        print(query)
        results = await db.execute(
            select(self.model).filter(*criterion).where(column.ilike(f"%{expr}%"))
        )
        return results.scalars().first()

    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        if settings.PREFER_DATABASE_DESCENDING:
            results = await db.execute(
                select(self.model)
                .order_by(self.model.id.desc())
                .offset(skip)
                .limit(limit)
            )
        else:
            results = await db.execute(select(self.model).offset(skip).limit(limit))
        return results.scalars().all()

    async def get_multi_filter(
        self, db: AsyncSession, criterion: Tuple, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        if settings.PREFER_DATABASE_DESCENDING:
            results = await db.execute(
                select(self.model)
                .filter(*criterion)
                .order_by(self.model.id.desc())
                .offset(skip)
                .limit(limit)
            )
        else:
            results = await db.execute(
                select(self.model).filter(*criterion).offset(skip).limit(limit)
            )
        return results.scalars().all()

    async def get_multi_filter_all(
        self, db: AsyncSession, criterion: Tuple
    ) -> List[ModelType]:
        results = await db.execute(select(self.model).filter(*criterion))
        return results.scalars().all()

    async def get_multi_filter_all_model(
        self, db: AsyncSession, model: ModelType, criterion: Tuple
    ) -> Any:
        results = await db.execute(select(model).filter(*criterion))
        return results.scalars().all()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, id: int) -> ModelType:
        obj = await db.get(self.model, id)
        await db.delete(obj)
        await db.commit()
        return obj

    async def remove_all(self, db: AsyncSession) -> int:
        objs = await db.execute(select(self.model))
        rows_deleted = 0
        for obj in objs:
            rows_deleted += await obj.delete()
        await db.commit()
        return rows_deleted

    async def remove_filter(self, db: AsyncSession, criterion: Tuple) -> int:
        objs = await db.execute(select(self.model).filter(*criterion))
        rows_deleted = 0
        for obj in objs:
            rows_deleted += await obj.delete()
        await db.commit()
        return rows_deleted

    async def remove_filter_model(
        self, db: AsyncSession, model: ModelType, criterion: Tuple
    ) -> int:
        objs = await db.execute(select(model).filter(*criterion))
        rows_deleted = 0
        for obj in objs:
            rows_deleted += await obj.delete()
        await db.commit()
        return rows_deleted
