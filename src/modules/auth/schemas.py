from typing import Optional

from pydantic import BaseModel, EmailStr

from modules.user.schemas import UserSchema


class LoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str


class RegisterRequest(BaseModel):
    name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class AuthorizedUserResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserSchema
