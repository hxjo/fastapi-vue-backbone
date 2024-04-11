from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db_url = settings.SQLALCHEMY_DATABASE_URI.unicode_string()  # type: ignore
    engine = create_async_engine(db_url, echo=settings.DEBUG_SQL)
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
