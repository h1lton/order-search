from typing import AsyncGenerator, Any

from sqlalchemy import JSON, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr

from .config import settings

metadata = MetaData()


class BaseModel(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}
    metadata = metadata

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Class name 'UserModel' -> table name 'user',
        that is, the class name must be in the format '<table_name>Model'.
        """
        return cls.__name__[:-5].lower()


engine = create_async_engine(settings.DB_DSN, echo=settings.DB_ECHO)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
