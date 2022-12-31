from sqlalchemy import Table, CHAR, Column, DateTime, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from app.database import Base


class RadUserGroup(Base):
    __tablename__ = Table("radusergroup", Base.metadata)

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    groupname = Column(String(64), nullable=False, server_default=text("''"))
    priority = Column(INTEGER(11), nullable=False, server_default=text("1"))
