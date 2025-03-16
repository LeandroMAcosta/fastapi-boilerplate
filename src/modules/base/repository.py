from contextlib import asynccontextmanager

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import get_async_db


class BaseRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_db)):
        self.session = session

    @classmethod
    async def get_instance(cls, session: AsyncSession = Depends(get_async_db)):
        """Provides an instance of the repository using dependency injection."""
        return cls(session)

    @asynccontextmanager
    async def get_session(self):
        """
        Provides a managed async session.
        Ensures the session is committed or rolled back properly.
        """
        try:
            yield self.session
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
