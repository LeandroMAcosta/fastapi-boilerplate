from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from modules.auth.schemas import AuthorizedUserResponse, LoginRequest, RegisterRequest
from modules.auth.service import AuthService
from modules.user.models import User
from modules.user.schemas import UserSchema
from modules.auth.google_service import GoogleAuthService

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


@router.get("/google/login")
async def google_login(google_service: GoogleAuthService = Depends()):
    """Redirect to Google OAuth consent screen"""
    auth_url = google_service.get_auth_url()
    return auth_url
    # return RedirectResponse(url=auth_url)


@router.get("/google/callback")
async def google_callback(
    code: str,
    google_service: GoogleAuthService = Depends(),
    auth_service: AuthService = Depends()
) -> AuthorizedUserResponse:
    """Handle Google OAuth callback"""
    user = await google_service.verify_google_token(code)
    access_token = auth_service.create_access_token(user)
    return AuthorizedUserResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserSchema.model_validate(user)
    )
