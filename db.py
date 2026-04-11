from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

Database_URl ="postgresql+asyncpg://user:2103@localhost/fastapi1"

engine=create_async_engine(Database_URl)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
