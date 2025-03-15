import json
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from core.config import settings
from modules.user.models import User
from modules.user.schemas import UserSchema
from modules.user.service import UserService

from .exceptions import InvalidCredentialsException
from .schemas import LoginRequest, RegisterRequest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
password_hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    user_service: UserService

    def __init__(self, user_service: UserService = Depends()):
        self.password_hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_service = user_service

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hashing.verify(plain_password, hashed_password)

    async def authenticate_user(self, auth_user: LoginRequest) -> User:
        username, email = auth_user.username, auth_user.email
        if not (username or email):
            raise InvalidCredentialsException()

        user: User | None = None
        if username:
            user = await self.user_service.get_by_username(username)
        elif email:
            user = await self.user_service.get_by_email(email)

        if not user:
            raise InvalidCredentialsException()

        is_verified = self.verify_password(auth_user.password, user.hashed_password)
        if not is_verified:
            raise InvalidCredentialsException()

        return user

    async def register_user(self, new_user_request: RegisterRequest) -> User:
        hashed_password = self.password_hashing.hash(new_user_request.password)
        new_user = User(
            name=new_user_request.name,
            last_name=new_user_request.last_name,
            username=new_user_request.username,
            email=new_user_request.email,
            hashed_password=hashed_password,
        )
        return await self.user_service.create(new_user)

    @staticmethod
    def create_access_token(user: User) -> str:
        access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION_TIME)
        access_token_payload = {
            "sub": json.dumps(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.name,
                    "last_name": user.last_name,
                }
            ),
            "exp": datetime.now(timezone.utc) + access_token_expires,
        }

        access_token = jwt.encode(
            access_token_payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
        return access_token.decode("utf-8")

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
        """
        Get the current user from the request.
        """
        try:
            decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user_data = json.loads(decoded_token["sub"])
            return UserSchema(**user_data)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except (jwt.DecodeError, jwt.InvalidTokenError) as e:
            raise HTTPException(status_code=401, detail="Invalid token")
