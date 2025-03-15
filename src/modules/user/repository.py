from sqlalchemy.future import select

from modules.base.repository import BaseRepository
from modules.user.exceptions import UserNotFoundException
from modules.user.models import User


class UserRepository(BaseRepository):

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Get a user by ID.
        """
        async with self.get_session() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            return result.scalars().first()

    async def create(self, user: User) -> User:
        """
        Create a new user in the database.
        """
        async with self.get_session() as session:
            session.add(user)
            await session.flush()
            await session.refresh(user)
            return user

    async def fetch_by_username(self, username: str) -> User | None:
        """
        Fetch a user by username. Returns None if not found.
        """
        async with self.get_session() as session:
            stmt = select(User).where(User.username == username)
            result = await session.execute(stmt)
            return result.scalars().first()

    async def get_by_username(self, username: str) -> User:
        """
        Get a user by username. Raises UserNotFoundException if not found.
        """
        user = await self.fetch_by_username(username)
        if not user:
            raise UserNotFoundException()
        return user

    async def fetch_by_email(self, email: str) -> User | None:
        """
        Fetch a user by email. Returns None if not found.
        """
        async with self.get_session() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            return result.scalars().first()

    async def get_by_email(self, email: str) -> User:
        """
        Get a user by email. Raises UserNotFoundException if not found.
        """
        user = await self.fetch_by_email(email)
        if not user:
            raise UserNotFoundException()
        return user
