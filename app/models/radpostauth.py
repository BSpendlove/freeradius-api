from sqlalchemy import Table, CHAR, Column, DateTime, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from app.database import Base


class RadPostAuth(Base):
    __tablename__ = Table("radpostauth", Base.metadata)

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    _pass = Column("pass", String(64), nullable=False, server_default=text("''"))
    reply = Column(String(32), nullable=False, server_default=text("''"))
    authdate = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
    )
