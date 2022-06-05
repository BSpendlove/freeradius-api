from enum import Enum

from pydantic import BaseModel


class OpEnum(str, Enum):
    equals = "="
    compare = ":="
    append = "+="
