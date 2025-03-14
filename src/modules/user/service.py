from typing import Optional

from fastapi import Depends
from pydantic import EmailStr

from modules.user.models import User
from modules.user.repository import UserRepository


class UserService:

    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.user_repo.get_by_id(user_id)

    def create(self, user: User) -> User:
        return self.user_repo.create(user)

    def fetch_by_username(self, username: str) -> Optional[User]:
        return self.user_repo.fetch_by_username(username)

    def get_by_username(self, username: str) -> User:
        return self.user_repo.get_by_username(username)

    def fetch_by_email(self, email: EmailStr) -> Optional[User]:
        return self.user_repo.fetch_by_email(email)

    def get_by_email(self, email: EmailStr) -> User:
        return self.user_repo.get_by_email(email)


# def get_user_service() -> UserService:
#     return UserService()
