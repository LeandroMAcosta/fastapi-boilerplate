from typing import Optional

from fastapi import Depends
from pydantic import EmailStr

from modules.user.models import User
from modules.user.repository import UserRepository
from modules.user.exceptions import UserAlreadyExistsException


class UserService:

    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.user_repo.get_by_id(user_id)

    async def create(self, user: User) -> User:
        existing_user = await self.fetch_by_email(user.email)
        if existing_user:
            raise UserAlreadyExistsException(field="email")
        
        existing_user = await self.fetch_by_username(user.username)
        if existing_user:
            raise UserAlreadyExistsException(field="username")

        return await self.user_repo.create(user)

    async def fetch_by_username(self, username: str) -> Optional[User]:
        return await self.user_repo.fetch_by_username(username)

    async def get_by_username(self, username: str) -> User:
        return await self.user_repo.get_by_username(username)

    async def fetch_by_email(self, email: EmailStr) -> Optional[User]:
        return await self.user_repo.fetch_by_email(email)

    async def get_by_email(self, email: EmailStr) -> User:
        return await self.user_repo.get_by_email(email)
