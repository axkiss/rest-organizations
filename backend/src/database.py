from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.config import settings

engine = create_async_engine(settings.database.async_database_url, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Model(DeclarativeBase):
    pass


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
