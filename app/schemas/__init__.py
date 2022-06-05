# Core Schema Imports
from .nas import NAS, NASCreate, NASInDB, NASUpdate
from .radacct import RadAcct, RadAcctCreate, RadAcctInDB, RadAcctUpdate
from .radgroupcheck import (
    RadGroupCheck,
    RadGroupCheckCreate,
    RadGroupCheckInDB,
    RadGroupCheckUpdate,
)
from .radgroupreply import (
    RadGroupReply,
    RadGroupReplyCreate,
    RadGroupReplyInDB,
    RadGroupReplyUpdate,
)
from .radpostauth import (
    RadPostAuth,
    RadPostAuthCreate,
    RadPostAuthInDB,
    RadPostAuthUpdate,
)
from .radcheck import RadCheck, RadCheckCreate, RadCheckInDB, RadCheckUpdate
from .radreply import RadReply, RadReplyCreate, RadReplyInDB, RadReplyUpdate
from .radusergroup import (
    RadUserGroup,
    RadUserGroupCreate,
    RadUserGroupInDB,
    RadUserGroupUpdate,
)
from .generic import GenericDeleteResponse
from .user import RadiusUser
from .group import RadiusGroup

# Custom Schema Imports
from .extended.coa import COABase, COAAVPair, COAResponse
