from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


# This example assumes you store the sessionmaker in the app state during startup.
# If not, you can import your sessionmaker directly.
async def get_async_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    Retrieves the sessionmaker from the app state.
    """
    async with request.app.state.session_local() as session:
        yield session


def init_db():
    """
    Initializes the database engine and sessionmaker.
    This function should be called in main.py during server startup.
    """
    DATABASE_URI = settings.POSTGRES_URI
    DATABASE_PREFIX = settings.POSTGRES_ASYNC_PREFIX
    DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

    engine = create_async_engine(DATABASE_URL, echo=settings.DEBUG, future=True)
    session_local = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    return engine, session_local
