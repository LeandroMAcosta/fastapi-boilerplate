from inspect import isawaitable

import pytest
from fastapi import HTTPException

from modules.auth.exceptions import InvalidCredentialsException
from modules.auth.schemas import LoginRequest, RegisterRequest
from modules.auth.service import AuthService
from modules.user.models import User


@pytest.mark.asyncio(loop_scope="function")
async def test_register_user(auth_service: AuthService):
    register_request = RegisterRequest(
        username="newuser", email="new@example.com", password="password123", name="New", last_name="User"
    )

    user = await auth_service.register_user(register_request)
    assert user.id is not None
    assert user.username == register_request.username
    assert user.email == register_request.email
    assert user.name == register_request.name
    assert user.last_name == register_request.last_name


# @pytest.mark.asyncio
# async def test_authenticate_user_with_username(auth_service: AuthService, test_user: User):
#     login_request = LoginRequest(
#         username="testuser",
#         password="password123"
#     )

#     user = await auth_service.authenticate_user(login_request)
#     assert user.id == test_user.id
#     assert user.username == test_user.username


@pytest.mark.asyncio
async def test_authenticate_user_with_email(auth_service: AuthService, test_user: User):
    login_request = LoginRequest(email="test@example.com", password="mypassword123")

    user = await auth_service.authenticate_user(login_request)
    assert user.id == test_user.id
    assert user.email == test_user.email


# @pytest.mark.asyncio
# async def test_authenticate_user_invalid_credentials(auth_service: AuthService):
#     login_request = LoginRequest(
#         username="testuser",
#         password="wrongpassword"
#     )

#     with pytest.raises(InvalidCredentialsException):
#         await auth_service.authenticate_user(login_request)


@pytest.mark.asyncio
async def test_create_access_token(auth_service: AuthService, test_user: User):
    # Make sure to await test_user if it's a coroutine
    user = await test_user if isawaitable(test_user) else test_user
    token = auth_service.create_access_token(user)
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(auth_service: AuthService):
    with pytest.raises(HTTPException) as exc_info:
        auth_service.get_current_user("invalid_token")
    assert exc_info.value.status_code == 401
