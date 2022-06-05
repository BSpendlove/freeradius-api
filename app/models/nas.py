from sqlalchemy import Table, CHAR, Column, DateTime, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from app.database import Base, engine


class NAS(Base):
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
