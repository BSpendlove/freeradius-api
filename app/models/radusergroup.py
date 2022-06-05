from sqlalchemy import Table, CHAR, Column, DateTime, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from app.database import Base, engine


class RadUserGroup(Base):
    __tablename__ = Table(
        "radusergroup", Base.metadata, autoload=True, autoload_with=engine
    )

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    groupname = Column(String(64), nullable=False, server_default=text("''"))
    priority = Column(INTEGER(11), nullable=False, server_default=text("1"))
