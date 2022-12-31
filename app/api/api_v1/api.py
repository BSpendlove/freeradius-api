from fastapi import APIRouter

# Native API Routes
from app.api.api_v1.endpoints import nas
from app.api.api_v1.endpoints import radacct
from app.api.api_v1.endpoints import radgroupcheck
from app.api.api_v1.endpoints import radgroupreply
from app.api.api_v1.endpoints import radpostauth
from app.api.api_v1.endpoints import radcheck
from app.api.api_v1.endpoints import radreply
from app.api.api_v1.endpoints import radusergroup

# Friendlier API Routes (assosicate and add users/groups in a more API friendly way)
from app.api.api_v1.endpoints import users
from app.api.api_v1.endpoints import groups

# Extended API Routes (vendor specific modules, etc...)
from app.api.api_v1.extended import coa
from app.api.api_v1.extended import services

api_router = APIRouter()

# Native API Routes (Directly interact with the database tables)
api_router.include_router(nas.router, prefix="/radius/nas", tags=["nas"])
api_router.include_router(radacct.router, prefix="/radius/radacct", tags=["radacct"])
api_router.include_router(
    radgroupcheck.router, prefix="/radius/radgroupcheck", tags=["radgroupcheck"]
)
api_router.include_router(
    radgroupreply.router, prefix="/radius/radgroupreply", tags=["radgroupreply"]
)
api_router.include_router(
    radpostauth.router, prefix="/radius/radpostauth", tags=["radpostauth"]
)
api_router.include_router(radcheck.router, prefix="/radius/radcheck", tags=["radcheck"])
api_router.include_router(radreply.router, prefix="/radius/radreply", tags=["radreply"])
api_router.include_router(
    radusergroup.router, prefix="/radius/radusergroup", tags=["radusergroup"]
)

# Friendlier API Routes (assosicate and add users/groups in a more API friendly way)
api_router.include_router(users.router, prefix="/radius/users", tags=["users"])
api_router.include_router(groups.router, prefix="/radius/groups", tags=["groups"])

# Extended API Routes
api_router.include_router(coa.router, prefix="/radius/coa", tags=["coa"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
