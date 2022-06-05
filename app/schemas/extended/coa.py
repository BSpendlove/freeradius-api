from typing import Optional, List

from pydantic import BaseModel

from app.schemas.enums import OpEnum


class COAAVPair(BaseModel):
    attribute: str
    value: str

    def normalize_attribute(self) -> None:
        self.attribute = self.attribute.replace("-", "_")


class COABase(BaseModel):
    secret: str
    port: Optional[int] = 3799
    timeout: Optional[int] = 5
    attributes: Optional[List[COAAVPair]]


class COAResponse(BaseModel):
    code: int
    message: str
