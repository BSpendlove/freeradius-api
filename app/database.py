from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.config.app import settings

# Example of non-async database setup
# engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
# local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async Support
async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, poolclass=NullPool
)
async_local_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()
