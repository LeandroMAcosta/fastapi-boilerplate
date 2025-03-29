from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    """Raised when a user is not found."""

    def __init__(self) -> None:
        super().__init__(detail="User not found", status_code=404)

class UserAlreadyExistsException(HTTPException):
    def __init__(self, field: str):
        self.field = field
        super().__init__(detail=f"User with this {field} already exists", status_code=400)
