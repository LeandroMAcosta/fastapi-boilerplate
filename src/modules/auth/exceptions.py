from fastapi import HTTPException


class InvalidCredentialsException(HTTPException):
    """Raised when provided credentials (e.g., username or password) are invalid."""

    def __init__(self) -> None:
        super().__init__(detail="Invalid credentials", status_code=401)


class TokenExpiredException(HTTPException):
    """Raised when a JWT token has expired and is no longer valid."""

    def __init__(self) -> None:
        super().__init__(detail="Token expired", status_code=403)


class TokenVerificationException(HTTPException):
    """Raised when there is an issue verifying the authenticity of a JWT token."""

    def __init__(self) -> None:
        super().__init__(detail="Token verification failed", status_code=403)


class UnauthorizedAccessException(HTTPException):

    def __init__(
        self,
    ) -> None:
        super().__init__(detail="You do not have permission to access this resource", status_code=401)
