from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import settings
from typing import AsyncGenerator


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def init_db():
    import models  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await engine.dispose()
