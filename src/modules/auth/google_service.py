from fastapi import Depends
from google.oauth2 import id_token
from google.auth.transport import requests
from typing import Optional
import httpx

from core.config import settings
from modules.user.service import UserService
from modules.user.models import User

class GoogleAuthService:
    def __init__(
        self, 
        user_service: UserService = Depends()
    ):
        self.user_service = user_service
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI

    def get_auth_url(self) -> str:
        """Generate Google OAuth2 authorization URL"""
        return (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.client_id}&"
            "response_type=code&"
            f"redirect_uri={self.redirect_uri}&"
            "scope=email profile"
        )

    async def verify_google_token(self, code: str) -> Optional[User]:
        """Exchange auth code for tokens and verify user info"""
        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }

        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data)
            token_response.raise_for_status()
            tokens = token_response.json()

        # Verify ID token
        id_info = id_token.verify_oauth2_token(
            tokens["id_token"], 
            requests.Request(), 
            self.client_id
        )

        # Check if user exists
        user = await self.user_service.fetch_by_email(id_info["email"])
        
        if not user:
            # Create new user if doesn't exist
            user = User(
                email=id_info["email"],
                name=id_info.get("given_name", ""),
                last_name=id_info.get("family_name", ""),
                username=id_info["email"].split("@")[0],  # Use email prefix as username
                hashed_password=""  # Empty as Google auth doesn't need password
            )
            user = await self.user_service.create(user)

        return user 