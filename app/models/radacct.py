from sqlalchemy import Table, CHAR, Column, DateTime, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from app.database import Base, engine


class RadAcct(Base):
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
