import pytest
from fastapi import HTTPException

from modules.user.exceptions import UserNotFoundException
from modules.user.models import User
from modules.user.service import UserService


@pytest.mark.asyncio
async def test_create_user(user_service: UserService):
    user = User(username="newuser", email="new@example.com", hashed_password="hashedpass", name="New", last_name="User")
    created_user = await user_service.create(user)

    assert created_user.id is not None
    assert created_user.username == "newuser"
    assert created_user.email == "new@example.com"


@pytest.mark.asyncio
async def test_get_user_by_id(user_service: UserService, test_user: User):
    user = await user_service.get_by_id(test_user.id)
    assert user is not None
    assert user.id == test_user.id
    assert user.username == test_user.username


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_service: UserService):
    user = await user_service.get_by_id(999)
    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_username(user_service: UserService, test_user: User):
    user = await user_service.get_by_username(test_user.username)
    assert user is not None
    assert user.username == test_user.username


@pytest.mark.asyncio
async def test_get_user_by_username_not_found(user_service: UserService):
    with pytest.raises(UserNotFoundException):
        await user_service.get_by_username("nonexistent")


@pytest.mark.asyncio
async def test_get_user_by_email(user_service: UserService, test_user: User):
    user = await user_service.get_by_email(test_user.email)
    assert user is not None
    assert user.email == test_user.email


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(user_service: UserService):
    with pytest.raises(UserNotFoundException):
        await user_service.get_by_email("nonexistent@example.com")
