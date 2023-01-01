from enum import Enum
from typing import Optional, List, Union, Type
from pydantic import BaseModel, constr
from uuid import UUID

from app.schemas.radusergroup import RadUserGroup
from app.schemas.radcheck import RadCheck
from app.schemas.radreply import RadReply
from app.schemas.radgroupcheck import RadGroupCheck
from app.schemas.radgroupreply import RadGroupReply


class ServiceUsernameTypeEnum(str, Enum):
    str = "str"
    int = "int"
    uuid = "uuid"
    regex = "regex"
    mac_address = "mac_address"


class Service(BaseModel):
    service_name: constr(min_length=1, max_length=60)
    username_type: ServiceUsernameTypeEnum = ServiceUsernameTypeEnum.str
    username_regex: Optional[str]
    radusergroups: Optional[List[RadUserGroup]]
    radcheck_avpairs: Optional[List[RadCheck]]
    radreply_avpairs: Optional[List[RadReply]]
    radgroupcheck_avpairs: Optional[List[RadGroupCheck]]
    radgroupreply_avpairs: Optional[List[RadGroupReply]]
    prechecks_passed: bool = False


class ServiceCreateUser(BaseModel):
    service_name: str
    username: str
