from pydantic import BaseModel
from enum import Enum
from typing import List, Optional, Union
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network


class OpEnum(str, Enum):
    equals = "="
    compare = ":="
    append = "+="


class RadiusAttributeBase(BaseModel):
    attribute: str
    op: OpEnum
    value: str


class RadiusAttribute(RadiusAttributeBase):
    id: int

    class Config:
        orm_mode = True


class RadiusAttributeCreate(RadiusAttributeBase):
    pass


class RadiusAttributeDelete(RadiusAttributeBase):
    pass


class RadiusUserGroupBase(BaseModel):
    groupname: str
    priority: Optional[str]


class RadiusUserGroup(RadiusUserGroupBase):
    id: int
    username: str

    class Config:
        orm_mode = True


class RadiusUserBase(BaseModel):
    username: str


class RadiusUser(RadiusUserBase):
    radcheck: Optional[List[RadiusAttribute]]
    radreply: Optional[List[RadiusAttribute]]
    radusergroup: Optional[List[RadiusUserGroupBase]]


class RadiusUserCreate(RadiusUserBase):
    password: Optional[
        str
    ]  # Password is optional, BNG typically uses a 'fake' password and authenticates on something like User-Name attribute in PPPoE
    # (or IPoE where option-82 is copied into the User-Name attribute)... You should only pass this variable into the class
    # if you are planning on adding user specific attributes such as: Framed-IP, Loopback, VRF, etc...
    # Otherwise if you create a user without a password, you will need to send a PATCH since the POST will return error for a duplicate user
    groupname: str


class RadiusGroupBase(BaseModel):
    groupname: str


class RadiusGroup(RadiusGroupBase):
    radgroupcheck: Optional[List[RadiusAttribute]]
    radgroupreply: Optional[List[RadiusAttribute]]
    radusergroup: Optional[List[RadiusUserBase]]


class RadiusGroupCreate(RadiusGroupBase):
    password: Optional[
        str
    ] = "default"  # Password is optional but default, BNG typically uses a 'fake' password and authenticates on something like User-Name attribute in PPPoE
    # (or IPoE where option-82 is copied into the User-Name attribute)... You should only pass this variable into the class
    # if you are planning on adding user specific attributes such as: Framed-IP, Loopback, VRF, etc...
    # Otherwise if you create a user without a password, you will need to send a PATCH since the POST will return error for a duplicate user


class RadiusGroupDelete(RadiusGroupBase):
    pass


class RadiusPostAuthenticationBase(BaseModel):
    username: str
    _pass: str
    reply: str
    authdate: datetime

    class Config:
        fields = {"_pass": "pass"}


class RadiusPostAuthentication(RadiusPostAuthenticationBase):
    id: int

    class Config:
        orm_mode = True


class RadiusUserAccountingBase(BaseModel):
    acctsessionid: str
    acctuniqueid: str
    username: str
    nasipaddress: str
    calledstationid: str
    callingstationid: str
    acctterminatecause: str
    framedipaddress: str
    framedipv6address: str
    framedipv6prefix: str
    framedinterfaceid: str
    delegatedipv6prefix: str


class RadiusUserAccounting(RadiusUserAccountingBase):
    realm: Optional[str]
    realm: Optional[str]
    radacctid: Optional[int]
    nasportid: Optional[str]
    nasporttype: Optional[str]
    acctstarttime: Optional[datetime]
    acctupdatetime: Optional[datetime]
    acctstoptime: Optional[datetime]
    acctinterval: Optional[int]
    acctsessiontime: Optional[int]
    acctauthentic: Optional[str]
    connectinfo_start: Optional[str]
    connectinfo_stop: Optional[str]
    acctinputoctets: Optional[int]
    acctoutputoctets: Optional[int]
    servicetype: Optional[str]
    framedprotocol: Optional[str]

    class Config:
        orm_mode = True


class IANAPrivateEnterprise(BaseModel):
    decimal: int
    organization: str
    contact: Optional[str]
    email: Optional[str]


class VendorSpecificAttributeBase(BaseModel):
    vendor_id: int
    attribute_id: int
    attribute_type: Union[str, int, IPv4Address, IPv6Address, IPv4Network, IPv6Network]


# FreeRADIUS Vendors and Attributes
class FreeRADIUSVendor(BaseModel):
    # http://www.iana.org/enterprise-numbers.txt
    vendor_name: str
