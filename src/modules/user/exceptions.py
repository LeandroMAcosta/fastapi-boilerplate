from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    """Raised when a user is not found."""

    def __init__(self) -> None:
        super().__init__(detail="User not found", status_code=404)
