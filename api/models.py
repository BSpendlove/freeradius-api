"""Auto-generated using sqlacodegen against freeradius's schema.sql

Provided here: https://github.com/FreeRADIUS/freeradius-server/blob/master/raddb/mods-config/sql/main/mysql/schema.sql

If you have customized your database, install sqlacodegen and regenerate the models to be able to reference them in your code.
"""
from sqlalchemy import Table, CHAR, Column, DateTime, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from .database import Base, engine


class RadiusNAS(Base):
    __tablename__ = Table("nas", Base.metadata, autoload=True, autoload_with=engine)

    id = Column(INTEGER(10), primary_key=True)
    nasname = Column(String(128), nullable=False, index=True)
    shortname = Column(String(32))
    type = Column(String(30), server_default=text("'other'"))
    ports = Column(INTEGER(5))
    secret = Column(String(60), nullable=False, server_default=text("'secret'"))
    server = Column(String(64))
    community = Column(String(50))
    description = Column(String(200), server_default=text("'RADIUS Client'"))


class RadiusAccounting(Base):
    __tablename__ = Table("radacct", Base.metadata, autoload=True, autoload_with=engine)

    radacctid = Column(BIGINT(21), primary_key=True)
    acctsessionid = Column(
        String(64), nullable=False, index=True, server_default=text("''")
    )
    acctuniqueid = Column(
        String(32), nullable=False, unique=True, server_default=text("''")
    )
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    realm = Column(String(64), server_default=text("''"))
    nasipaddress = Column(
        String(15), nullable=False, index=True, server_default=text("''")
    )
    nasportid = Column(String(15))
    nasporttype = Column(String(32))
    acctstarttime = Column(DateTime, index=True)
    acctupdatetime = Column(DateTime)
    acctstoptime = Column(DateTime, index=True)
    acctinterval = Column(INTEGER(12), index=True)
    acctsessiontime = Column(INTEGER(12), index=True)
    acctauthentic = Column(String(32))
    connectinfo_start = Column(String(50))
    connectinfo_stop = Column(String(50))
    acctinputoctets = Column(BIGINT(20))
    acctoutputoctets = Column(BIGINT(20))
    calledstationid = Column(String(50), nullable=False, server_default=text("''"))
    callingstationid = Column(String(50), nullable=False, server_default=text("''"))
    acctterminatecause = Column(String(32), nullable=False, server_default=text("''"))
    servicetype = Column(String(32))
    framedprotocol = Column(String(32))
    framedipaddress = Column(
        String(15), nullable=False, index=True, server_default=text("''")
    )
    framedipv6address = Column(
        String(45), nullable=False, index=True, server_default=text("''")
    )
    framedipv6prefix = Column(
        String(45), nullable=False, index=True, server_default=text("''")
    )
    framedinterfaceid = Column(
        String(44), nullable=False, index=True, server_default=text("''")
    )
    delegatedipv6prefix = Column(
        String(45), nullable=False, index=True, server_default=text("''")
    )


class RadiusCheck(Base):
    __tablename__ = Table(
        "radcheck", Base.metadata, autoload=True, autoload_with=engine
    )

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    attribute = Column(String(64), nullable=False, server_default=text("''"))
    op = Column(CHAR(2), nullable=False, server_default=text("'=='"))
    value = Column(String(253), nullable=False, server_default=text("''"))


class RadiusGroupCheck(Base):
    __tablename__ = Table(
        "radgroupcheck", Base.metadata, autoload=True, autoload_with=engine
    )

    id = Column(INTEGER(11), primary_key=True)
    groupname = Column(
        String(64), nullable=False, index=True, server_default=text("''")
    )
    attribute = Column(String(64), nullable=False, server_default=text("''"))
    op = Column(CHAR(2), nullable=False, server_default=text("'=='"))
    value = Column(String(253), nullable=False, server_default=text("''"))


class RadiusGroupReply(Base):
    __tablename__ = Table(
        "radgroupreply", Base.metadata, autoload=True, autoload_with=engine
    )

    id = Column(INTEGER(11), primary_key=True)
    groupname = Column(
        String(64), nullable=False, index=True, server_default=text("''")
    )
    attribute = Column(String(64), nullable=False, server_default=text("''"))
    op = Column(CHAR(2), nullable=False, server_default=text("'='"))
    value = Column(String(253), nullable=False, server_default=text("''"))


class RadiusPostAuth(Base):
    __tablename__ = Table(
        "radpostauth", Base.metadata, autoload=True, autoload_with=engine
    )

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    _pass = Column("pass", String(64), nullable=False, server_default=text("''"))
    reply = Column(String(32), nullable=False, server_default=text("''"))
    authdate = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
    )


class RadiusReply(Base):
    __tablename__ = Table(
        "radreply", Base.metadata, autoload=True, autoload_with=engine
    )

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    attribute = Column(String(64), nullable=False, server_default=text("''"))
    op = Column(CHAR(2), nullable=False, server_default=text("'='"))
    value = Column(String(253), nullable=False, server_default=text("''"))


class RadiusUserGroup(Base):
    __tablename__ = Table(
        "radusergroup", Base.metadata, autoload=True, autoload_with=engine
    )

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    groupname = Column(String(64), nullable=False, server_default=text("''"))
    priority = Column(INTEGER(11), nullable=False, server_default=text("1"))
