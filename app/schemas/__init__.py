# Core Schema Imports
from app.schemas.nas import NAS, NASCreate, NASInDB, NASUpdate
from app.schemas.radacct import RadAcct, RadAcctCreate, RadAcctInDB, RadAcctUpdate
from app.schemas.radgroupcheck import (
    RadGroupCheck,
    RadGroupCheckCreate,
    RadGroupCheckInDB,
    RadGroupCheckUpdate,
)
from app.schemas.radgroupreply import (
    RadGroupReply,
    RadGroupReplyCreate,
    RadGroupReplyInDB,
    RadGroupReplyUpdate,
)
from app.schemas.radpostauth import (
    RadPostAuth,
    RadPostAuthCreate,
    RadPostAuthInDB,
    RadPostAuthUpdate,
)
from app.schemas.radcheck import RadCheck, RadCheckCreate, RadCheckInDB, RadCheckUpdate
from app.schemas.radreply import RadReply, RadReplyCreate, RadReplyInDB, RadReplyUpdate
from app.schemas.radusergroup import (
    RadUserGroup,
    RadUserGroupCreate,
    RadUserGroupInDB,
    RadUserGroupUpdate,
)
from app.schemas.generic import GenericDeleteResponse
from app.schemas.user import RadiusUser, RadiusUserCreate, RadiusUserUpdate
from app.schemas.group import RadiusGroup, RadiusGroupCreate, RadiusGroupUpdate

# Custom Schema Imports
from app.schemas.extended.coa import COABase, COAAVPair, COAResponse
