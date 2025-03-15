from fastapi import APIRouter, Depends

from modules.auth.schemas import AuthorizedUserResponse, LoginRequest, RegisterRequest
from modules.auth.service import AuthService
from modules.user.models import User
from modules.user.schemas import UserSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(auth_user: LoginRequest, auth_service: AuthService = Depends()) -> AuthorizedUserResponse:
    user = await auth_service.authenticate_user(auth_user)
    access_token = auth_service.create_access_token(user)
    return AuthorizedUserResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserSchema.model_validate(user),
    )


@router.post("/register")
async def register(auth_user: RegisterRequest, auth_service: AuthService = Depends()) -> AuthorizedUserResponse:
    user = await auth_service.register_user(auth_user)
    access_token = auth_service.create_access_token(user)
    return AuthorizedUserResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserSchema.model_validate(user),
    )


@router.get("/me")
async def me(current_user: UserSchema = Depends(AuthService.get_current_user)) -> UserSchema:
    return current_user
