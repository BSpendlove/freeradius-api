from sqlalchemy import Table, CHAR, Column, DateTime, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from app.database import Base, engine


class RadGroupCheck(Base):
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
