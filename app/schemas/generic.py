from typing import Optional

from pydantic import BaseModel

from app.schemas.enums import OpEnum


class GenericDeleteResponse(BaseModel):
    rows_deleted: int


class AVPair(BaseModel):
    id: Optional[int]
    attribute: str
    op: OpEnum
    value: str
